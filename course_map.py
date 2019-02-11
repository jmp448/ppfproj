from helpers import *
from read_transcript import *



def main():
    classes = read_transcript('transcript.xlsx')
    reqs = designate_reqs()
    reqs = fill_reqs(classes, reqs)

    for req in reqs:
        if req.taken:
            print(req.course.desc)


if __name__ == "__main__":
    main()
