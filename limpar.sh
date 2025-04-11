#!/bin/bash
git-filter-repo --invert-paths --force --paths-from-file <(cat <<EOF
dataset/maio2019.csv
dataset/abril2020.csv
dataset/abril2019.csv
dataset/maro2019.csv
dataset/maro2020.csv
dataset/agosto2018.csv
dataset/fevereiro2020.csv
dataset/julho2018.csv
dataset/maio2018.csv
EOF
)

