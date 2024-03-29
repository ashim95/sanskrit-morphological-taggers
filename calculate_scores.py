import sys


def load_file(filename):

    gold_tags = []
    pred_tags = []

    keys = []

    with open(filename, 'r') as fp:
        for line in fp:
            text = line.strip()
            if text.startswith('word'):
                keys = text.split('\t')[1:]
            elif len(text) == 0:
                continue
            else:
                tags = text.split('\t')[1:]
                g = {}
                p = {}
                for i, key in enumerate(keys):
                    g[key] = tags[i].split(':')[0]
                    p[key] = tags[i].split(':')[1]
                gold_tags.append(g)
                pred_tags.append(p)

    print("Total words : " + str(len(gold_tags)))

    return gold_tags, pred_tags

def computeF1(hyps, golds, prefix, labels_to_ix=None, write_results=False):


    f1_precision_scores = {}
    f1_precision_total = {}
    f1_recall_scores = {}
    f1_recall_total = {}
    f1_average = 0.0

    # Precision
    for i, word_tags in enumerate(hyps, start=0):
        for k, v in word_tags.items():
            if v=="999":
                continue
            if k not in f1_precision_scores:
                f1_precision_scores[k] = 0
                f1_precision_total[k] = 0
            if k in golds[i]:
                if v==golds[i][k]:
                    f1_precision_scores[k] += 1
            f1_precision_total[k] += 1

    #print(f1_precision_scores)
    #print(f1_precision_total)
    f1_micro_precision = sum(f1_precision_scores.values())/sum(f1_precision_total.values())

    for k in f1_precision_scores.keys():
        f1_precision_scores[k] = f1_precision_scores[k]/f1_precision_total[k]

    # Recall
    for i, word_tags in enumerate(golds, start=0):
        for k, v in word_tags.items():
            if v=="999":
                continue
            if k not in f1_recall_scores:
                f1_recall_scores[k] = 0
                f1_recall_total[k] = 0
            if k in hyps[i]:
                if v==hyps[i][k]:
                    f1_recall_scores[k] += 1
            f1_recall_total[k] += 1

    #print(f1_recall_scores)
    #print(f1_recall_total)
    f1_micro_recall = sum(f1_recall_scores.values())/sum(f1_recall_total.values())

    f1_scores = {}

    for k in f1_recall_scores.keys():
        f1_recall_scores[k] = f1_recall_scores[k]/f1_recall_total[k]
        if f1_recall_scores[k]==0 or k not in f1_precision_scores:
            f1_scores[k] = 0
        else:
            f1_scores[k] = 2 * (f1_precision_scores[k] * f1_recall_scores[k]) / (f1_precision_scores[k] + f1_recall_scores[k])

        f1_average += f1_recall_total[k] * f1_scores[k]

    f1_average /= sum(f1_recall_total.values())
    f1_micro_score = 2 * (f1_micro_precision * f1_micro_recall) / (f1_micro_precision + f1_micro_recall)

    f1_scores_categories = {}
    for k, v in f1_precision_scores.items():
        f1_scores_categories[k] = 2 * (f1_precision_scores[k] * f1_recall_scores[k]) / (f1_precision_scores[k] + f1_recall_scores[k])

    #print("--"*40)
    #print("Printing Precision/Recall Scores -- ")
    #print(f1_precision_scores)
    #print(f1_recall_scores)
    #print("F-Scores")
    #print(f1_scores_categories)
    #print("--"*40)
    #print("Printing Macro-F1 , Micro-F1 --")
    #print(f1_average, f1_micro_score)
    #print("--"*40)
    return f1_average, f1_micro_score

def get_exact_accuracy(gold_tags, pred_tags):

    # inputs: list of dicts
    correct = 0
    total = 0
    for i, g in enumerate(gold_tags):
        p = pred_tags[i]
        total +=1
        if p == g:
            correct +=1

    #print("--"*40)
    print("Total Correct :" + str(correct))
    print("Total         :" + str(total))
    print("Exact Token Accuracy :" + str(correct/(float(total))))
    #print("--"*40)
    return correct/(float(total))

def get_average(gold_tags, pred_tags):

    scores = []

    for i, gt in enumerate(gold_tags):
        pt = pred_tags[i]
        correct = 0
        for k, v in gt.items():
            if v == pt[k]:
                correct +=1
        scores.append(correct/float(len(gt)))

    return scores


if __name__=="__main__":

    comparison_file = sys.argv[1]
    num_sets = int(sys.argv[2])
    set_size = int(sys.argv[3])

    all_gold_tags, all_pred_tags = load_file(comparison_file)

    results = []

    average = []

    start = 0
    for set_no in range(num_sets):
        print("\n")
        print("--"*40)
        print("--"*40)
        print("Printing Statistics for Set {0}".format(set_no))
        gold = all_gold_tags[start:start + set_size * 4]
        pred = all_pred_tags[start:start + set_size * 4]
        start = start + set_size * 4
        print("Total Words : " + str(len(gold)))

        f1_average, f1_micro_score = computeF1(pred, gold, '')

        acc = get_exact_accuracy(gold, pred)
        avg_scores = get_average(gold, pred)
        average.append(sum(avg_scores)/(4 * set_size))
        results.append(acc)
        print("--"*40)
        print("--"*40)

    print(results)
    for res in results:
        print(res)
    print("Averages....")
    for a in average:
        print(a)


