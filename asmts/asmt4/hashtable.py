class HashTable:
    def __init__(self, hash_fn, capacity=1009):
        self.hf = hash_fn
        self._capacity = capacity
        self._buckets = [[] for _ in range(self._capacity)]
        self._count = 0
    
    def _hash(self, key: str) -> int:
        
        raw = self.hf(key)
        return raw % self._capacity
    
    def size(self) -> int:

        return self._count
    
    def put(self, key: str, value: tuple) -> None:
        idx = self._hash(key)
        bucket = self._buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        
        bucket.append(key, value)
        self._count += 1
    
    def get(self, key: str):
        idx = self._hash(key)
        bucket = self._buckets[idx]
        for (k, v) in bucket:
            if k == key:
                return v
        raise KeyError(f"Key not found: {key}")
    
    def probe(self, key: str) -> bool:
        idx = self._hash(key)
        return any(k == key for (k, _) in self._buckets[idx])
    
    def delete(self, key: str):
        idx = self._hash(key)
        bucket = self._buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self._count -= 1
                return
        raise KeyError(f"Key not found: {key}")
    
    def all_keys(self):
        return [k for bucket in self._buckets for (k, _) in bucket]

