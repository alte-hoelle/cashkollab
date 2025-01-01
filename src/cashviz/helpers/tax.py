from cashviz.models.journal_entry import JournalEntry


def clean_from_tax(incident: JournalEntry) -> float:
    if incident.taxes == 0:
        return float(incident.signed)
    return float(incident.signed * 100 / (100 + incident.taxes))
