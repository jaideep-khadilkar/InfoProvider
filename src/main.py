import gmail


def main():
    info_form_list = gmail.extract_info()
    for info_form in info_form_list:
        print info_form
        print '<<<-------------->>>'


if __name__ == '__main__':
    main()