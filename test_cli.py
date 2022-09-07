import sys
import tracker

if __name__ == '__main__':
    """
    Usage:
        rating_url
        candidate_id
        columns 
    """
    # TODO Колонка с оригиналами=False или ищи сколько оригиналов в списке
    # TODO Подписи для выбранных колонок

    print('cmd entry:', sys.argv)

    rating_url = sys.argv[1]
    candidate_id = sys.argv[2]
    columns = [int(i) for i in sys.argv[3].split(',')]

    a = tracker.do_request(rating_url, candidate_id, columns=columns)

    # TODO записать то, что получилось в базу, где id = md5(url + id + cols)
