"""Offline Master-table projections, kept separate from observed account values.

Projection uses cumulative thresholds. It does not assert that the supplied
Master snapshot matches the live service or an installed client's hotfixes.
"""
from __future__ import annotations

import hashlib
import json
from bisect import bisect_right
from pathlib import Path

from tools.growth_export import ExportError, MAX_BYTES, MAX_RECORDS, MAX_SAFE_INTEGER

TABLES = ('MemberCard', 'MemberCardLevel', 'SupportCard', 'SupportCardLevel',
          'CharacterRank', 'Vip')


def number(value):
    if type(value) is not int or not 0 <= value <= MAX_SAFE_INTEGER:
        raise ExportError('invalid_projection_number')
    return value


class Thresholds:
    def __init__(self, rows, value_key, level_key):
        pairs = sorted((number(r[value_key]), number(r[level_key])) for r in rows)
        if not pairs or pairs[0][0] != 0 or pairs[0][1] != 1:
            raise ExportError('invalid_level_table_origin')
        if any(b[0] <= a[0] or b[1] != a[1] + 1 for a, b in zip(pairs, pairs[1:])):
            raise ExportError('ambiguous_level_thresholds')
        self.values, self.levels = zip(*pairs)

    def resolve(self, value):
        return self.levels[bisect_right(self.values, number(value)) - 1]


class GrowthLevels:
    def __init__(self, master_dir: Path):
        tables, digest = {}, hashlib.sha256()
        try:
            for name in TABLES:
                path = master_dir / ('Master' + name + '.json')
                if path.stat().st_size > MAX_BYTES:
                    raise ExportError('master_table_too_large')
                raw = path.read_bytes()
                digest.update(name.encode() + b'\0' + len(raw).to_bytes(8, 'big') + raw)
                rows = json.loads(raw)['_allData']
                if not isinstance(rows, list) or len(rows) > MAX_RECORDS:
                    raise ExportError('invalid_master_rows')
                tables[name] = rows
            self.cards = {}
            for kind, prefix, group_key in (
                ('memberCards', 'MemberCard', '_memberCardLevelGroup'),
                ('supportCards', 'SupportCard', '_supportCardLevelGroup'),
            ):
                groups = {}
                for row in tables[prefix + 'Level']:
                    groups.setdefault(number(row['_group']), []).append(row)
                levels = {g: Thresholds(rows, '_exp', '_level') for g, rows in groups.items()}
                cards = {}
                for row in tables[prefix]:
                    card_id, group = number(row['_id']), number(row[group_key])
                    if card_id in cards or group not in levels:
                        raise ExportError('invalid_master_card_mapping')
                    cards[card_id] = levels[group]
                self.cards[kind] = cards
            self.characters = Thresholds(tables['CharacterRank'], '_exp', '_rank')
            self.tgw = Thresholds(tables['Vip'], '_point', '_vipRank')
            self.digest = digest.hexdigest()
        except (KeyError, TypeError, ValueError, OSError) as exc:
            if isinstance(exc, ExportError):
                raise
            raise ExportError('invalid_master_tables') from None

    def derive(self, growth):
        """Return only public IDs and projected levels; never mutate observations."""
        result = {'memberCards': None, 'supportCards': None, 'characterRanks': None,
                  'tgw': None}
        unresolved = 0
        try:
            for kind, cards in self.cards.items():
                source = growth.get(kind)
                if source is None:
                    continue
                if not isinstance(source, list) or len(source) > MAX_RECORDS:
                    raise ExportError('invalid_projection_collection')
                result[kind] = []
                for record in source:
                    card_id, exp = number(record['masterId']), number(record['exp'])
                    level = cards[card_id].resolve(exp) if card_id in cards else None
                    unresolved += level is None
                    result[kind].append({'masterId': card_id, 'level': level})
            source = growth.get('characterRanks')
            if source is not None:
                if not isinstance(source, list) or len(source) > MAX_RECORDS:
                    raise ExportError('invalid_projection_collection')
                result['characterRanks'] = [{'characterId': number(r['characterId']),
                    'rank': self.characters.resolve(r['exp'])} for r in source]
            if growth.get('tgw') is not None:
                result['tgw'] = {'level': self.tgw.resolve(growth['tgw']['point'])}
        except (KeyError, TypeError):
            raise ExportError('invalid_growth_projection_input') from None
        return {'method': 'cumulative_master_thresholds', 'masterTablesSha256': self.digest,
                'verification': 'table_projection_not_ui_reconciled',
                'unresolvedCardCount': unresolved, 'growth': result}
