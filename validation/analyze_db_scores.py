import pickle
import matplotlib.pyplot as plt
import statistics

if __name__ == "__main__":
    with open('all_scores.pickle', 'rb') as handle:
        results = pickle.load(handle)

    scores = [row[3] for row in results]
    n = 500
    buckets = [scores[i:i + n] for i in range(0, len(scores), n)]
    print(buckets)
    print(len(buckets))
    bucket_means = []
    for bucket in buckets:
        bucket_means.append(statistics.mean(bucket))

    plt.xlabel('sorted buckets by RMSD (bucket size - {}). total unique sequences - {}'.format(n, len(scores)))
    plt.ylabel('DB mean score')
    plt.title('DB mean score vs sorted buckets by RMSD (bucket size - {})'.format(n))
    plt.plot(bucket_means)
    plt.savefig('1000_bucket_scores.png')
    plt.show()
