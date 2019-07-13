#! /bin/sh
# A simple HTML file merge scripts.
# Author:
# Version: 0.1
# Merge HTML files in given folder and generate a mono html file called "all_in_one.html"
# User can specify an index file which contains a list of all files in chapter order, and
# if not specified, the script will use 'ls' to list all files that need to be merged.
#

TARGET="all_in_one.html"
#clean result and intermediate files from last run
rm -vf ${TARGET} toc.tag *.sed index.list

# default html tag tokens
TOKEN_TOC='<div class="toc">'
TOKEN_CHAP_PREFIX='<span class="chapter"><a href="'
TOKEN_CHAP_NAME='[0-9a-zA-Z,\_]+\.html'
TOKEN_BODY_BEG='<body>'
TOKEN_BODY_END='</body>'
TOKEN_HTML_BEG='<html>'
TOKEN_HTML_END='</html>'
# use extended regex
GREP='egrep'
SED='sed'
# debug only
#html_path='html'
#index_page='index.html'

print_usage()
{
    printf  "./merge_html.sh [OPTIONS] html_path [index_page]\n"
    printf  "PARAMETERS:\n"
    printf  "\thtml_path  Path to html files need to be merged.\n"
    printf  "\tindex_page The html file which contains toc(table of contents).\
If not provided, the html files will be merged in the order of 'ls' output.\n"
    printf  "OPTIONS:\n"
    printf  "\t--tok-toc  Overide the toc(table of contents) pattern.\n"
    printf  "\t--tok-prefix  Overide the html file tag prefix pattern. \
This will be used to address the html file name.\n"
    printf  "\t--tok-name  Overide the html file name pattern.\n"
    printf  "\t-h|--help print this help message.\n"

}

# sed script1: remove address token and trailing "
cat>rm_addr_tok.sed<<EOF
{
    s/${TOKEN_CHAP_PREFIX}//g
    s/\"$//g
}
EOF
# sed script2: replace thumbnail image file name with the regular one
cat>rm_tb_pic.sed<<EOF
{
    s/\-[0-9]\{3\}x[0-9]\{3\}\.jpg/\.jpg/g
    s/\-[0-9]\{3\}x[0-9]\{3\}\.png/\.png/g
}
EOF
# sed script3: remove html and body begin tag in each chapter
cat>rm_html_tag.sed<<EOF
{
    s;${TOKEN_HTML_BEG};;g
    s;${TOKEN_BODY_BEG};;g
    s;${TOKEN_BODY_END};;g
    s;${TOKEN_HTML_END};;g
}
EOF

# parameters
index_page_default="index.html"
html_path=
index_page=
USE_LS_RESULT=

PARSED_OPT=`getopt -o h --long tok-toc:,tok-prefix:,tok-name:,help\
           -n "$0" -- "$@"`
if [ $? != 0 ] ; then echo "Terminating..." >&2 ; exit 1 ; fi

eval set -- "$PARSED_OPT"

while true;do
    case "$1" in
        --tok-toc)
            TOKEN_TOC="$2"
            echo "TOKEN_TOC: ${TOKEN_TOC}"
            shift 2 ;;
        --tok-prefix)
            TOKEN_CHAP_PREFIX="$2"
            echo "TOKEN_CHAP_PREFIX: ${TOKEN_CHAP_PREFIX}"
            shift 2 ;;
        --tok-name) TOKEN_CHAP_NAME="$2"
            echo "TOKEN_CHAP_NAME: ${TOKEN_CHAP_NAME}"
            shift 2 ;;
        -h|--help) print_usage; shift ; exit 0 ;;
        --) shift ; break ;;    # delimter of non-option arguments
        *) echo " Internal error!" ; exit 1 ;;
    esac
done
# now processing non-option arguments...
if [[ -z "$@" ]]; then
    read -p "Please specify the folder of html files need to be merged: " html_path
else
    for arg do
        if [[ -d $arg ]]; then
            html_path=$arg
        elif [[ -n $html_path && -f "$html_path/$arg" ]]; then
            IS_HTML=`egrep -o "^$TOKEN_HTML_BEG|$TOKEN_HTML_END$" "$html_path/$arg"`
            if [[ -z "$IS_HTML" ]]; then
                echo "Not a html file, try again." ; exit 1
            fi
            index_page=$arg
        fi
    done
fi

if [[ -z "$html_path" ]]; then
    echo "No html files path specified. Exit."
    exit 1
elif [[ -z "$index_page" ]]; then
    echo "No index file specified, use 'ls' result instead."
    USE_LS_RESULT=1
fi

if [[ -z $USE_LS_RESULT ]]; then
    echo "Trying to extract TOC from index page... "
    ${GREP} -o "${TOKEN_TOC}" "$html_path/$index_page" > toc.tag
    if [[ -s toc.tag ]]; then
        ${GREP} "${TOKEN_TOC}" $html_path/$index_page |${GREP} -o \
        "${TOKEN_CHAP_PREFIX}${TOKEN_CHAP_NAME}" | ${SED} -f rm_addr_tok.sed > index.list
    else
        # fall back to 'ls' result
        echo "No table of contents found in index page. Will use file order in $html_path"
        # index_page must be excluded from toc ...
        ls -t $html_path |${GREP} -iv "$index_page" > index.list
    fi
else
    # index_page must be excluded from toc ...
    ls -t $html_path |${GREP} -iv "$index_page_default" > index.list
fi

echo "TOC: "
cat index.list

echo "Merging html files ... "
for i in $(< index.list)
do
#   sed -f rm_tb_pic.sed -i "$html_path/$i"
    sed -f rm_html_tag.sed "$html_path/$i" >> ${TARGET}
done
echo "${TOKEN_BODY_END}${TOKEN_HTML_END}" >> ${TARGET}
echo "Merged result:  ${TARGET}"
