import time
import random
from typing import Optional
from fortune_models.models import FortunePool, FortuneEntry
from fortune_triggers.triggers import FortuneTriggers


def find_applicable_trigger_for_pool(pool: FortunePool):
    """Analyzes all possible fortune triggers and gets first which returned True
    and which exists in the specified pool."""
    for trigger in FortuneTriggers().get_applicable_triggers():
        if pool.fortuneentry_set.filter(trigger__iexact=trigger).count() > 0:
            return trigger


def find_applicable_entry(pool: FortunePool) -> Optional[FortuneEntry]:
    applicable_trigger = find_applicable_trigger_for_pool(pool)
    found_entries = FortuneEntry.objects.filter(trigger__exact=applicable_trigger, pool=pool)
    seed = int(time.time() / pool.entry_expiration_seconds)

    if not found_entries:
        return None

    random.seed(seed)
    return random.choice(found_entries)
