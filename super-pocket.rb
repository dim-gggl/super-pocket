class SuperPocket < Formula
  include Language::Python::Virtualenv

  desc "Developer toolkit: README generator, codebase-to-markdown, XML tags, agent templates & cheatsheets"
  homepage "https://github.com/dim-gggl/super-pocket"
  url "https://github.com/dim-gggl/super-pocket/archive/refs/tags/v1.0.2.tar.gz"
  sha256 "d6d15536ffb24636b1a21d3a0806260e8b6939cca29904529175dfb76f35fe19"
  license "MIT"

  option "with-docs", "Include documentation build dependencies (Sphinx stack)"
  option "with-dev", "Include development dependencies (pytest stack)"

  depends_on "python@3.11"

  depends_on "rust" => :build

  depends_on "freetype"
  depends_on "jpeg-turbo"
  depends_on "libtiff"
  depends_on "little-cms2"
  depends_on "openjpeg"
  depends_on "webp"
  depends_on "zlib"
 
  depends_on "pkg-config" => :build

  # ------------------------------------------------------------
  # CORE DEPENDENCIES
  # ------------------------------------------------------------
  resource "rich-click" do
    url "https://files.pythonhosted.org/packages/bf/d8/f2c1b7e9a645ba40f756d7a5b195fc104729bc6b19061ba3ab385f342931/rich_click-1.9.4.tar.gz"
    sha256 "af73dc68e85f3bebb80ce302a642b9fe3b65f3df0ceb42eb9a27c467c1b678c8"
  end
  
  resource "click" do
    url "https://files.pythonhosted.org/packages/3d/fa/656b739db8587d7b5dfa22e22ed02566950fbfbcdc20311993483657a5c0/click-8.3.1.tar.gz"
    sha256 "12ff4785d337a1bb490bb7e9c2b1ee5da3112e94a8622f26a6c77f5d2fc6842a"
  end
  
  resource "pillow" do
    url "https://files.pythonhosted.org/packages/5a/b0/cace85a1b0c9775a9f8f5d5423c8261c858760e2466c79b2dd184638b056/pillow-12.0.0.tar.gz"
    sha256 "87d4f8125c9988bfbed67af47dd7a953e2fc7b0cc1e7800ec6d2080d490bb353"
  end
  
  resource "pyyaml" do
    url "https://files.pythonhosted.org/packages/05/8e/961c0007c59b8dd7729d542c61a4d537767a59645b82a0b521206e1e25c2/pyyaml-6.0.3.tar.gz"
    sha256 "d76623373421df22fb4cf8817020cbb7ef15c725b9d5e45f17e189bfc384190f"
  end
  
  resource "urllib3" do
    url "https://files.pythonhosted.org/packages/15/22/9ee70a2574a4f4599c47dd506532914ce044817c7752a79b6a51286319bc/urllib3-2.5.0.tar.gz"
    sha256 "3fc47733c7e419d4bc3f6b3dc2b4f890bb743906a30d56ba4a5bfa4bbff92760"
  end

  resource "idna" do
    url "https://files.pythonhosted.org/packages/6f/6d/0703ccc57f3a7233505399edb88de3cbd678da106337b9fcde432b65ed60/idna-3.11.tar.gz"
    sha256 "795dafcc9c04ed0c1fb032c2aa73654d8e8c5023a7df64a53f39190ada629902"
  end

  resource "certifi" do
    url "https://files.pythonhosted.org/packages/a2/8c/58f469717fa48465e4a50c014a0400602d3c437d7c0c468e17ada824da3a/certifi-2025.11.12.tar.gz"
    sha256 "d8ab5478f2ecd78af242878415affce761ca6bc54a22a27e026d7c25357c3316"
  end

  resource "annotated-types" do
    url "https://files.pythonhosted.org/packages/ee/67/531ea369ba64dcff5ec9c3402f9f51bf748cec26dde048a2f973a4eea7f5/annotated_types-0.7.0.tar.gz"
    sha256 "aff07c09a53a08bc8cfccb9c85b05f1aa9a2a6f23728d790723543408344ce89"
  end

  resource "anyio" do
    url "https://files.pythonhosted.org/packages/c6/78/7d432127c41b50bccba979505f272c16cbcadcc33645d5fa3a738110ae75/anyio-4.11.0.tar.gz"
    sha256 "82a8d0b81e318cc5ce71a5f1f8b5c4e63619620b63141ef8c995fa0db95a57c4"
  end

  resource "charset-normalizer" do
    url "https://files.pythonhosted.org/packages/13/69/33ddede1939fdd074bce5434295f38fae7136463422fe4fd3e0e89b98062/charset_normalizer-3.4.4.tar.gz"
    sha256 "94537985111c35f28720e43603b8e7b43a6ecfb2ce1d3058bbe955b73404e21a"
  end

  resource "colorama" do
    url "https://files.pythonhosted.org/packages/d8/53/6f443c9a4a8358a93a6792e2acffb9d9d5cb0a5cfd8802644b7b1c9a02e4/colorama-0.4.6.tar.gz"
    sha256 "08695f5cb7ed6e0531a20572697297273c47b8cae5a63ffc6d6ed5c201be6e44"
  end

  resource "h11" do
    url "https://files.pythonhosted.org/packages/01/ee/02a2c011bdab74c6fb3c75474d40b3052059d95df7e73351460c8588d963/h11-0.16.0.tar.gz"
    sha256 "4e35b956cf45792e4caa5885e69fba00bdbc6ffafbfa020300e549b208ee5ff1"
  end

  resource "httpcore" do
    url "https://files.pythonhosted.org/packages/06/94/82699a10bca87a5556c9c59b5963f2d039dbd239f25bc2a63907a05a14cb/httpcore-1.0.9.tar.gz"
    sha256 "6e34463af53fd2ab5d807f399a9b45ea31c3dfa2276f15a2c3f00afff6e176e8"
  end

  resource "packaging" do
    url "https://files.pythonhosted.org/packages/a1/d4/1fc4078c65507b51b96ca8f8c3ba19e6a61c8253c72794544580a7b6c24d/packaging-25.0.tar.gz"
    sha256 "d443872c98d677bf60f6a1f2f8c1cb748e8fe762d2bf9d3148b5599295b0fc4f"
  end

  resource "pydantic" do
    url "https://files.pythonhosted.org/packages/96/ad/a17bc283d7d81837c061c49e3eaa27a45991759a1b7eae1031921c6bd924/pydantic-2.12.4.tar.gz"
    sha256 "0f8cb9555000a4b5b617f66bfd2566264c4984b27589d3b845685983e8ea85ac"
  end

  resource "pydantic-core" do
    url "https://files.pythonhosted.org/packages/71/70/23b021c950c2addd24ec408e9ab05d59b035b39d97cdc1130e1bce647bb6/pydantic_core-2.41.5.tar.gz"
    sha256 "08daa51ea16ad373ffd5e7606252cc32f07bc72b28284b6bc9c6df804816476e"
  end

  resource "requests" do
    url "https://files.pythonhosted.org/packages/c9/74/b3ff8e6c8446842c3f5c837e9c3dfcfe2018ea6ecef224c710c85ef728f4/requests-2.32.5.tar.gz"
    sha256 "dbba0bac56e100853db0ea71b82b4dfd5fe2bf6d3754a8893c3af500cec7d7cf"
  end

  resource "roman-numerals-py" do
    url "https://files.pythonhosted.org/packages/30/76/48fd56d17c5bdbdf65609abbc67288728a98ed4c02919428d4f52d23b24b/roman_numerals_py-3.1.0.tar.gz"
    sha256 "be4bf804f083a4ce001b5eb7e3c0862479d10f94c936f6c4e5f250aa5ff5bd2d"
  end

  resource "six" do
    url "https://files.pythonhosted.org/packages/94/e7/b2c673351809dca68a0e064b6af791aa332cf192da575fd474ed7d6f16a2/six-1.17.0.tar.gz"
    sha256 "ff70335d468e7eb6ec65b95b99d3a2836546063f63acc5171de367e834932a81"
  end

  resource "sniffio" do
    url "https://files.pythonhosted.org/packages/a2/87/a6771e1546d97e7e041b6ae58d80074f81b7d5121207425c964ddf5cfdbd/sniffio-1.3.1.tar.gz"
    sha256 "f4324edc670a0f49750a81b895f35c3adb843cca46f0530f79fc1babb23789dc"
  end

  resource "starlette" do
    url "https://files.pythonhosted.org/packages/ba/b8/73a0e6a6e079a9d9cfa64113d771e421640b6f679a52eeb9b32f72d871a1/starlette-0.50.0.tar.gz"
    sha256 "a2a17b22203254bcbc2e1f926d2d55f3f9497f769416b3190768befe598fa3ca"
  end

  resource "typing-extensions" do
    url "https://files.pythonhosted.org/packages/72/94/1a15dd82efb362ac84269196e94cf00f187f7ed21c242792a923cdb1c61f/typing_extensions-4.15.0.tar.gz"
    sha256 "0cea48d173cc12fa28ecabc3b837ea3cf6f38c6d1136f85cbaaf598984861466"
  end

  resource "typing-inspection" do
    url "https://files.pythonhosted.org/packages/55/e3/70399cb7dd41c10ac53367ae42139cf4b1ca5f36bb3dc6c9d33acdb43655/typing_inspection-0.4.2.tar.gz"
    sha256 "ba561c48a67c5958007083d386c3295464928b01faa735ab8547c5692e87f464"
  end

  resource "watchfiles" do
    url "https://files.pythonhosted.org/packages/c2/c9/8869df9b2a2d6c59d79220a4db37679e74f807c559ffe5265e08b227a210/watchfiles-1.1.1.tar.gz"
    sha256 "a173cb5c16c4f40ab19cecf48a534c409f7ea983ab8fed0741304a1c0a31b3f2"
  end

  resource "websockets" do
    url "https://files.pythonhosted.org/packages/21/e6/26d09fab466b7ca9c7737474c52be4f76a40301b08362eb2dbc19dcc16c1/websockets-15.0.1.tar.gz"
    sha256 "82544de02076bafba038ce055ee6412d68da13ab47f0c60cab827346de828dee"
  end
 
  # ------------------------------------------------------------
  # DEV DEPENDENCIES
  # ------------------------------------------------------------
  if build.with? "dev"
    resource "coverage" do
      url "https://files.pythonhosted.org/packages/89/26/4a96807b193b011588099c3b5c89fbb05294e5b90e71018e065465f34eb6/coverage-7.12.0.tar.gz"
      sha256 "fc11e0a4e372cb5f282f16ef90d4a585034050ccda536451901abfb19a57f40c"
    end

    resource "iniconfig" do
      url "https://files.pythonhosted.org/packages/72/34/14ca021ce8e5dfedc35312d08ba8bf51fdd999c576889fc2c24cb97f4f10/iniconfig-2.3.0.tar.gz"
      sha256 "c76315c77db068650d49c5b56314774a7804df16fee4402c1f19d6d15d8c4730"
    end

    resource "pluggy" do
      url "https://files.pythonhosted.org/packages/f9/e2/3e91f31a7d2b083fe6ef3fa267035b518369d9511ffab804f839851d2779/pluggy-1.6.0.tar.gz"
      sha256 "7dcc130b76258d33b90f61b658791dede3486c3e6bfb003ee5c9bfb396dd22f3"
    end

    resource "pytest" do
      url "https://files.pythonhosted.org/packages/07/56/f013048ac4bc4c1d9be45afd4ab209ea62822fb1598f40687e6bf45dcea4/pytest-9.0.1.tar.gz"
      sha256 "3e9c069ea73583e255c3b21cf46b8d3c56f6e3a1a8f6da94ccb0fcf57b9d73c8"
    end
  end

  # ------------------------------------------------------------
  # DOCUMENTATION DEPENDENCIES
  # ------------------------------------------------------------
  if build.with? "docs"
    resource "alabaster" do
      url "https://files.pythonhosted.org/packages/a6/f8/d9c74d0daf3f742840fd818d69cfae176fa332022fd44e3469487d5a9420/alabaster-1.0.0.tar.gz"
      sha256 "c00dca57bca26fa62a6d7d0a9fcce65f3e026e9bfe33e9c538fd3fbb2144fd9e"
    end

    resource "annotated-doc" do
      url "https://files.pythonhosted.org/packages/57/ba/046ceea27344560984e26a590f90bc7f4a75b06701f653222458922b558c/annotated_doc-0.0.4.tar.gz"
      sha256 "fbcda96e87e9c92ad167c2e53839e57503ecfda18804ea28102353485033faa4"
    end

    resource "babel" do
      url "https://files.pythonhosted.org/packages/7d/6b/d52e42361e1aa00709585ecc30b3f9684b3ab62530771402248b1b1d6240/babel-2.17.0.tar.gz"
      sha256 "0c54cffb19f690cdcc52a3b50bcbf71e07a808d1c80d549f2459b9d2cf0afb9d"
    end

    resource "docutils" do
      url "https://files.pythonhosted.org/packages/ae/ed/aefcc8cd0ba62a0560c3c18c33925362d46c6075480bfa4df87b28e169a9/docutils-0.21.2.tar.gz"
      sha256 "3a6b18732edf182daa3cd12775bbb338cf5691468f91eeeb109deff6ebfa986f"
    end

    resource "imagesize" do
      url "https://files.pythonhosted.org/packages/a7/84/62473fb57d61e31fef6e36d64a179c8781605429fd927b5dd608c997be31/imagesize-1.4.1.tar.gz"
      sha256 "69150444affb9cb0d5cc5a92b3676f0b2fb7cd9ae39e947a5e11a36b4497cd4a"
    end

    resource "markdown-it-py" do
      url "https://files.pythonhosted.org/packages/5b/f5/4ec618ed16cc4f8fb3b701563655a69816155e79e24a17b651541804721d/markdown_it_py-4.0.0.tar.gz"
      sha256 "cb0a2b4aa34f932c007117b194e945bd74e0ec24133ceb5bac59009cda1cb9f3"
    end

    resource "MarkupSafe" do
      url "https://files.pythonhosted.org/packages/7e/99/7690b6d4034fffd95959cbe0c02de8deb3098cc577c67bb6a24fe5d7caa7/markupsafe-3.0.3.tar.gz"
      sha256 "722695808f4b6457b320fdc131280796bdceb04ab50fe1795cd540799ebe1698"
    end

    resource "mdit-py-plugins" do
      url "https://files.pythonhosted.org/packages/b2/fd/a756d36c0bfba5f6e39a1cdbdbfdd448dc02692467d83816dff4592a1ebc/mdit_py_plugins-0.5.0.tar.gz"
      sha256 "f4918cb50119f50446560513a8e311d574ff6aaed72606ddae6d35716fe809c6"
    end

    resource "mdurl" do
      url "https://files.pythonhosted.org/packages/d6/54/cfe61301667036ec958cb99bd3efefba235e65cdeb9c84d24a8293ba1d90/mdurl-0.1.2.tar.gz"
      sha256 "bb413d29f5eea38f31dd4754dd7377d4465116fb207585f97bf925588687c1ba"
    end

    resource "myst-parser" do
      url "https://files.pythonhosted.org/packages/66/a5/9626ba4f73555b3735ad86247a8077d4603aa8628537687c839ab08bfe44/myst_parser-4.0.1.tar.gz"
      sha256 "5cfea715e4f3574138aecbf7d54132296bfd72bb614d31168f48c477a830a7c4"
    end

    resource "Pygments" do
      url "https://files.pythonhosted.org/packages/b0/77/a5b8c569bf593b0140bde72ea885a803b82086995367bf2037de0159d924/pygments-2.19.2.tar.gz"
      sha256 "636cb2477cec7f8952536970bc533bc43743542f70392ae026374600add5b887"
    end

    resource "snowballstemmer" do
      url "https://files.pythonhosted.org/packages/75/a7/9810d872919697c9d01295633f5d574fb416d47e535f258272ca1f01f447/snowballstemmer-3.0.1.tar.gz"
      sha256 "6d5eeeec8e9f84d4d56b847692bacf79bc2c8e90c7f80ca4444ff8b6f2e52895"
    end

    resource "Sphinx" do
      url "https://files.pythonhosted.org/packages/38/ad/4360e50ed56cb483667b8e6dadf2d3fda62359593faabbe749a27c4eaca6/sphinx-8.2.3.tar.gz"
      sha256 "398ad29dee7f63a75888314e9424d40f52ce5a6a87ae88e7071e80af296ec348"
    end

    resource "sphinx-autobuild" do
      url "https://files.pythonhosted.org/packages/e0/3c/a59a3a453d4133777f7ed2e83c80b7dc817d43c74b74298ca0af869662ad/sphinx_autobuild-2025.8.25.tar.gz"
      sha256 "9cf5aab32853c8c31af572e4fecdc09c997e2b8be5a07daf2a389e270e85b213"
    end

    resource "sphinx-autodoc-typehints" do
      url "https://files.pythonhosted.org/packages/34/4f/4fd5583678bb7dc8afa69e9b309e6a99ee8d79ad3a4728f4e52fd7cb37c7/sphinx_autodoc_typehints-3.5.2.tar.gz"
      sha256 "5fcd4a3eb7aa89424c1e2e32bedca66edc38367569c9169a80f4b3e934171fdb"
    end

    resource "sphinx-rtd-theme" do
      url "https://files.pythonhosted.org/packages/91/44/c97faec644d29a5ceddd3020ae2edffa69e7d00054a8c7a6021e82f20335/sphinx_rtd_theme-3.0.2.tar.gz"
      sha256 "b7457bc25dda723b20b086a670b9953c859eab60a2a03ee8eb2bb23e176e5f85"
    end

    resource "sphinx-tabs" do
      url "https://files.pythonhosted.org/packages/6a/53/a9a91995cb365e589f413b77fc75f1c0e9b4ac61bfa8da52a779ad855cc0/sphinx-tabs-3.4.7.tar.gz"
      sha256 "991ad4a424ff54119799ba1491701aa8130dd43509474aef45a81c42d889784d"
    end

    resource "sphinxcontrib-applehelp" do
      url "https://files.pythonhosted.org/packages/ba/6e/b837e84a1a704953c62ef8776d45c3e8d759876b4a84fe14eba2859106fe/sphinxcontrib_applehelp-2.0.0.tar.gz"
      sha256 "2f29ef331735ce958efa4734873f084941970894c6090408b079c61b2e1c06d1"
    end

    resource "sphinxcontrib-devhelp" do
      url "https://files.pythonhosted.org/packages/f6/d2/5beee64d3e4e747f316bae86b55943f51e82bb86ecd325883ef65741e7da/sphinxcontrib_devhelp-2.0.0.tar.gz"
      sha256 "411f5d96d445d1d73bb5d52133377b4248ec79db5c793ce7dbe59e074b4dd1ad"
    end

    resource "sphinxcontrib-htmlhelp" do
      url "https://files.pythonhosted.org/packages/43/93/983afd9aa001e5201eab16b5a444ed5b9b0a7a010541e0ddfbbfd0b2470c/sphinxcontrib_htmlhelp-2.1.0.tar.gz"
      sha256 "c9e2916ace8aad64cc13a0d233ee22317f2b9025b9cf3295249fa985cc7082e9"
    end

    resource "sphinxcontrib-httpdomain" do
      url "https://files.pythonhosted.org/packages/be/ef/82d3cfafb7febce4f7df8dcf3cde9d072350b41066e05a4f559b4e9105d0/sphinxcontrib-httpdomain-1.8.1.tar.gz"
      sha256 "6c2dfe6ca282d75f66df333869bb0ce7331c01b475db6809ff9d107b7cdfe04b"
    end

    resource "sphinxcontrib-jquery" do
      url "https://files.pythonhosted.org/packages/de/f3/aa67467e051df70a6330fe7770894b3e4f09436dea6881ae0b4f3d87cad8/sphinxcontrib-jquery-4.1.tar.gz"
      sha256 "1620739f04e36a2c779f1a131a2dfd49b2fd07351bf1968ced074365933abc7a"
    end

    resource "sphinxcontrib-jsmath" do
      url "https://files.pythonhosted.org/packages/b2/e8/9ed3830aeed71f17c026a07a5097edcf44b692850ef215b161b8ad875729/sphinxcontrib-jsmath-1.0.1.tar.gz"
      sha256 "a9925e4a4587247ed2191a22df5f6970656cb8ca2bd6284309578f2153e0c4b8"
    end

    resource "sphinxcontrib-qthelp" do
      url "https://files.pythonhosted.org/packages/68/bc/9104308fc285eb3e0b31b67688235db556cd5b0ef31d96f30e45f2e51cae/sphinxcontrib_qthelp-2.0.0.tar.gz"
      sha256 "4fe7d0ac8fc171045be623aba3e2a8f613f8682731f9153bb2e40ece16b9bbab"
    end

    resource "sphinxcontrib-serializinghtml" do
      url "https://files.pythonhosted.org/packages/3b/44/6716b257b0aa6bfd51a1b31665d1c205fb12cb5ad56de752dfa15657de2f/sphinxcontrib_serializinghtml-2.0.0.tar.gz"
      sha256 "e9d912827f872c029017a53f0ef2180b327c3f7fd23c87229f7a8e8b70031d4d"
    end
  end

  # ------------------------------------------------------------
  # INSTALLATION
  # ------------------------------------------------------------
  def install
   docs_resources = %w[
     alabaster
     annotated-doc
     babel
     docutils
     imagesize
     markdown-it-py
     MarkupSafe
     mdit-py-plugins
     mdurl
     myst-parser
     Pygments
     snowballstemmer
     Sphinx
     sphinx-autobuild
     sphinx-autodoc-typehints
     sphinx-rtd-theme
     sphinx-tabs
     sphinxcontrib-applehelp
     sphinxcontrib-devhelp
     sphinxcontrib-htmlhelp
     sphinxcontrib-httpdomain
     sphinxcontrib-jquery
     sphinxcontrib-jsmath
     sphinxcontrib-qthelp
     sphinxcontrib-serializinghtml
   ]

  dev_resources = %w[coverage iniconfig pluggy pytest]

  venv = virtualenv_create(libexec, "python3.11")

  resources.each do |resource|
    next if docs_resources.include?(resource.name) && build.without?("docs")
    next if dev_resources.include?(resource.name) && build.without?("dev")

    venv.pip_install resource
  end

   venv.pip_install_and_link buildpath
  end
 
  test do
    # Adapte selon le vrai output
    system bin/"pocket", "--help"
  end
 
  def caveats
    <<~EOS
      Super Pocket has been installed successfully!
 
      Run 'pocket --help' to get started.
 
      Note: This formula uses Python 3.11 exclusively due to binary wheel
      compatibility requirements for pydantic-core and watchfiles.

     Optional dependencies:
     - with-docs: installs the full Sphinx toolchain (themes, extensions,
       Markdown support). Enables local doc builds but increases download size
       and build time.
     - with-dev: installs pytest, coverage and helpers for running the project's
       test suite locally. Skipping it keeps the install smaller and faster.
    EOS
  end
end