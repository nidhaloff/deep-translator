# install the project and dependencies

git clone https://github.com/davideuler/pdf-translator-for-human
cd pdf-translator-for-human
pip install -e .
pip install streamlit pymupdf openai 

# Start the Web Application
streamlit run app.py