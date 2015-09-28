from optparse import OptionParser
import os
import pprint

ALL = 0
ONLY_YAML = 1
ALL_EXCEPT_YAML = 2
ONLY_DB = 3


def get_files(filter_mode=ALL, scale_size=1.0):
    _size_by_filename = {}
    for dirpath, dirnames, filenames in os.walk('.'):
        # print 'dirpath = ', dirpath
        for f in filenames:
            filepath = os.path.join(dirpath, f)
            if filter_mode == ONLY_DB and not filepath.endswith(".db"):
                continue
            elif filter_mode == ONLY_YAML and not filepath.endswith(".yaml"):
                continue
            elif filter_mode == ALL_EXCEPT_YAML and filepath.endswith(".yaml"):
                continue
            _size_by_filename[filepath] = round(os.path.getsize(filepath) * scale_size, 2)

    return _size_by_filename


def total_size(filter_mode=ALL, scale_size=1.0):
    _total_size = 0
    _num_files = 0

    for dirpath, dirnames, filenames in os.walk('.'):
        # print 'dirpath = ', dirpath
        for f in filenames:
            filepath = os.path.join(dirpath, f)
            # print 'filepath = ', filepath
            if filter_mode == ONLY_DB and not filepath.endswith(".db"):
                continue
            elif filter_mode == ONLY_YAML and not filepath.endswith(".yaml"):
                continue
            elif filter_mode == ALL_EXCEPT_YAML and filepath.endswith(".yaml"):
                continue
            _num_files += 1
            _total_size += round(os.path.getsize(filepath) * scale_size, 2)

    return _num_files, _total_size

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-l", "--list", action="store_true", dest="list_mode",  default=False)  # list or size mode
    parser.add_option("-k", "--kb", action="store_true", dest="is_size_kb",  default=False,
                      help="print size in kb")
    parser.add_option("-m", "--mb", action="store_true", dest="is_size_mb",  default=False,
                      help="print size in kb")
    parser.add_option("-f", "--filter", action="store", dest="filter_mode",  type="int", default=ALL,
                      help="0: all files, 1: ONLY yaml files, 2: all EXCEPT yaml files")

    (options, args) = parser.parse_args()

    scale_size = 1
    size_string = "bytes"
    if options.is_size_kb:
        scale_size = 1/1000.0
        size_string = "KB"
    elif options.is_size_mb:
        scale_size = 1/1000000.0
        size_string = "MB"

    if options.list_mode:
        # list file mode
        size_by_filename = get_files(options.filter_mode, scale_size=scale_size)
        for filename, size in size_by_filename.iteritems():
            print '{0}: {1} {2}'.format(filename, size, size_string)
    else:
        num_files, total_size = total_size(options.filter_mode, scale_size=scale_size)
        print 'total files = ', num_files
        print '{0} {1}'.format(total_size, size_string)
