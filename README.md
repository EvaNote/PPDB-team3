# PPDB-team3
Programming Project Databases 2019-2020: Campus Carpool

[![Build Status](https://travis-ci.com/EvaNote/PPDB-team3.svg?token=yq9VxQP8q1wzqhBqGKqA&branch=master)](https://travis-ci.com/EvaNote/PPDB-team3)

## How to use Flask-Babel
Every single bit of text that has to be translated should be wrapped in the function `gettext()`, or the shorter version `_()`.

- To extract the text to be translated, run `pybabel extract -F babel.cfg -k _l -o messages.pot .` in the root directory.
This will generate a `messages.pot` template file, which contains all bits of text that should be translated.

- To generate a language catalog, run `pybabel init -i messages.pot -d src/translations -l <lang>`, where `<lang>` is either
'en', 'fr' or 'nl'. This will create a directory `translations` in `src` (if it doesn't exist yet), and generate a new 
catalog with a `messages.po` file, where you can manually translate text.

- To compile the `messages.po` file(s), run `pybabel compile -d src/translations`, which will create a `messages.mo` file per 
`messages.po` file that wasn't compiled yet.

- If you added text to translate (by adding `_()`'s) without overwriting what you've already translated, run 
`pybabel extract -F babel.cfg -k _l -o messages.pot .` or `pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .` to update the template file, then run `pybabel update -i messages.pot -d src/translations`
to update the `messages.po` file(s). This last command will merge the already existing file with the newly generated one.
 