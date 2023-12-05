class MovigAverage():
    def __init__(self):
        self.sum = 0
        self.count = 0

    def update(self, value):
        self.sum += value
        self.count += 1

    def result(self):
        if self.count == 0:
            return 0
        return self.sum / self.count


class SameGroupSampler(Sampler):
    def __init__(self, df ,ds):
        super().__init__(ds)

        # Create a dictionary of posting_id -> index in dataset
        self.index_to_position = dict(zip(df.index, range(len(df))))

        # Create a Series of label_group -> set(posting_id)
        self.label_group = df.reset_index().groupby('label_group')['posting_id'].apply(set).map(sorted).map(np.array)

    def __len__(self):
        return len(self.label_group)

    def __iter__(self):
        for _ in range(len(self)):
            # Sample one label_group
            label_group_sample = self.label_group.sample(1).iloc[0]

            # Sample two posting_id's
            sample1, sample2 = np.random.choice(label_group_sample, 2, replace=False)

            yield self.index_to_position[sample1]
            yield self.index_to_position[sample2]
