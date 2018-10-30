import logging

import gmail

logging.basicConfig(level=logging.INFO)
logging.getLogger("googleapiclient").setLevel(logging.ERROR)
logger = logging.getLogger('AutoReply')


def main():
    logger.info('AutoReply script started.')
    logger.info('Reading gmail messages')
    info_form_list = gmail.Gmail().read_messages()
    output_file = open('results.txt', 'w')
    for info_form in info_form_list:
        output_file.write(str(info_form))
        output_file.write('\n<<<-------------->>>\n')
    output_file.close()
    logger.info('Reading Gmail messages completed. Please check results.txt')

if __name__ == '__main__':
    main()
