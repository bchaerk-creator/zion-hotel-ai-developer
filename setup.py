"""
Setup do Zion Hotel AI Developer.
"""

from setuptools import setup, find_packages

setup(
    name="zion-hotel-ai-developer",
    version="1.0.0",
    description="Agente de IA para Desenvolvimento Hoteleiro - Zion Hotel Group International",
    author="Zion Hotel Group International",
    author_email="contato@zionhotelgroup.com",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "openai>=1.30.0",
        "pydantic>=2.5.0",
        "rich>=13.7.0",
        "jinja2>=3.1.0",
        "pandas>=2.1.0",
        "numpy>=1.26.0",
        "python-dotenv>=1.0.0",
        "click>=8.1.0",
        "tabulate>=0.9.0",
        "httpx>=0.27.0",
        "pyyaml>=6.0.0",
    ],
    extras_require={
        # Coleta automática de prospects. Pesado (~100 pacotes) e exige
        # Python 3.12+, por isso fica fora da instalação padrão.
        "prospects": ["scrapegraphai>=2.2.2"],
        # tests/test_imports.py já usava pytest sem declará-lo em lugar nenhum
        "dev": ["pytest>=8.0.0"],
    },
    entry_points={
        "console_scripts": [
            "zion-ai=src.main:cli",
        ],
    },
)
