class Transaction:
    def __init__(self,
                 amount,
                 entry_type,
                 notes,
                 date,
                 currency='EURO',
                 tags=set(),
                 category=None):
        self.amount = amount
        self.entry_type = entry_type
        self.notes = notes
        self.date = date
        self.currency = currency
        self.tags = tags
        self.category = category
        
    def _set_tag(self, tag):
        self.tags.add(tag)

    def _set_category(self, category):
        self.category = category

    def _update_notes(self, note):
        self.notes = note