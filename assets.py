# compile stylesheets
python3 manage.py compilescss

# rename folders so they can be ignored
mv ${NODE}/material-design-lite/src ${NODE}/material-design-lite/src-ignore
mv ${NODE}/roboto-fontface/css ${NODE}/roboto-fontface/css-ignore

# copy static files into STATIC_DIR
python3 manage.py collectstatic --no-input \
    -i *.scss -i *.less \
    -i tiny_mce \
    -i src-ignore \
    -i css-ignore \
    --clear

# rename folders back
mv ${NODE}/material-design-lite/src-ignore ${NODE}/material-design-lite/src
mv ${NODE}/roboto-fontface/css-ignore ${NODE}/roboto-fontface/css

# compress stylesheets and javascripts
python3 manage.py compress --force
