from setuptools import setup, find_packages

setup(
    name="agent-modules",
    version="0.1.0",
    description="Agent Modules",
    author="idghst",
    packages=find_packages(include=["modules", "modules.*"]),
    install_requires=[
        "google-api-python-client",
        "google-auth-oauthlib",
        "google-auth-httplib2",
        "python-dotenv",
        "requests",
    ],
    python_requires=">=3.8",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
