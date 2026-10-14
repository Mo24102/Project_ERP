import json
import operator

OPERATORS = {
    "=": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
    "in": lambda a, b: a in b,
    "ilike": lambda a, b: str(b).lower() in str(a).lower(),
}


class Model:
    _name = None          # اسم الـ model زي 'sale.order'
    _defaults = {}        # قيم افتراضية
    _store = {}           # كل الداتا: {model_name: {id: record}}

    # ---------- مساعد داخلي ----------
    @classmethod
    def _table(cls):
        return cls._store.setdefault(cls._name, {})

    # ---------- CRUD ----------
    @classmethod
    def create(cls, vals):
        table = cls._table()
        new_id = max(table, default=0) + 1
        record = {**cls._defaults, **vals, "id": new_id}
        table[new_id] = record
        return new_id

    @classmethod
    def browse(cls, record_id):
        record = cls._table().get(record_id)
        if record is None:
            raise KeyError(f"{cls._name} id={record_id} not found")
        return dict(record)            # نسخة، عشان محدش يعدل بالغلط

    @classmethod
    def search(cls, domain=None):
        """domain مثال: [('state', '=', 'draft'), ('total', '>', 100)]"""
        domain = domain or []
        result = []
        for record in cls._table().values():
            if all(OPERATORS[op](record.get(field), value)
                   for field, op, value in domain):
                result.append(record["id"])
        return result

    @classmethod
    def write(cls, record_id, vals):
        cls.browse(record_id)          # يتأكد إنه موجود
        cls._table()[record_id].update(vals)
        return True

    @classmethod
    def unlink(cls, record_id):
        cls.browse(record_id)
        del cls._table()[record_id]
        return True

    # ---------- حفظ وتحميل ----------
    @classmethod
    def save_all(cls, path="data.json"):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cls._store, f, ensure_ascii=False, indent=2)

    @classmethod
    def load_all(cls, path="data.json"):
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except FileNotFoundError:
            return
        # JSON بيحوّل مفاتيح الأرقام لنصوص، فبنرجّعها أرقام
        cls._store = {
            model: {int(rid): rec for rid, rec in table.items()}
            for model, table in raw.items()
        }