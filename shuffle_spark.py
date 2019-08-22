def shuffle_rdd(rdd):
    swap = lambda x: (x[1], x[0])
    def add_random_key(it):
        seed = int(os.urandom(4).encode('hex'), 16)
        rs = np.random.RandomState(seed)
        return ((rs.rand(), swap(x)) for x in it)

    rdd_with_keys = (rdd.zipWithUniqueId().mapPartitions(add_random_key, preservesPartitioning=True))
    n = rdd.getNumPartitions()
    return rdd_with_keys.partitionBy(n).mapPartitions(sorted, preservesPartitioning=True).values().values()
