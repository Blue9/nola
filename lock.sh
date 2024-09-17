CUSTOM_COMPILE_COMMAND='./lock.sh' pip-compile requirements.in \
    --strip-extras \
    --quiet \
    --generate-hashes \
    --output-file requirements.txt
