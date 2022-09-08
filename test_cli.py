import sys
import tracker
import tracker_hist
import tracker_notify
import hashlib

DB_STATUS = {
    1: 'New subscribe',
    2: 'Changes detected'
}

if __name__ == '__main__':
    """
    Usage:
        rating_url
        candidate_id
        columns
        column_name
    """
    # TODO Колонка с оригиналами=False или ищи сколько оригиналов в списке
    # TODO План набора (кол-во)

    print('cmd entry:', sys.argv)

    rating_url = sys.argv[1]
    candidate_id = sys.argv[2]
    columns = [int(i) for i in sys.argv[3].split(',')]
    column_name = sys.argv[4].split(',')
    title = sys.argv[5]

    # rating_url = "https://sdo.mpgu.org/competition-list/entrant-list?cg=127&type=list"
    # candidate_id = "185-187-512 00"
    # columns = [0, 9]
    # column_name = ['Позиция', 'Балл']

    result, res_table = tracker.do_request(rating_url, candidate_id, columns=columns)

    message = ''
    for i in range(len(columns)):
        message += f'{column_name[i]}: {result[i]}\r\n'

    status = tracker_hist.check_subscribe(
        hashlib.md5((rating_url + candidate_id).encode('utf-8')).hexdigest(),
        message
    )
    print(status)

    if status == 1:
        message = f'Ты подписался на новый [список]({rating_url}) ({title}). \r\n' + message
    elif status == 2:
        message = f'Изменения в [список]({rating_url}) ({title}). \r\n' + message
    else:
        message = f'Изменений нет {title}\r\n' + message

    tracker_notify.send_message(message, parse_mode='Markdown')
    # TODO записать то, что получилось в базу, где id = md5(url + id + cols)
