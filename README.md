## EAnalyzer
Creative Essay scoring microservice to score articles from https://github.com/Dash-Off
Use the blackboard architecture pattern to build a creative essay scorer powered by PrithivirajDamodaran/Gramformer.
Contains grammar checker, vocabulary analyzer & relevance analyzer to score the creatives based on the challenges.

Install grammar checker:
`
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install -U git+https://github.com/PrithivirajDamodaran/Gramformer.git
python3 -m spacy download en_core_web_sm
`

Install Vocabulary Analyzer:
`pip install nltk spacy textstat`

Install Relevance analyzer
`pip install rake-nltk
pip install scikit-learn`

