const papers = [
  { year: 1990, journal: "RFS", title: "Pooling, Separating, and Semiseparating Equilibria in Financial Markets: Some Experimental Evidence", authors: "Charles B Cadsby, Murray Frank & Vojislav Maksimovic", type: ["lab"] },
  { year: 1991, journal: "JF", title: "Partial Revelation of Information in Experimental Asset Markets", authors: "Thomas E Copeland & Daniel Friedman", type: ["lab"] },
  { year: 1991, journal: "JF", title: "Dynamic Stock Markets with Multiple Assets: An Experimental Analysis", authors: "John O'brien & Sanjay Srivastava", type: ["lab", "market"] },
  { year: 1996, journal: "JF", title: "Call and Continuous Trading Mechanisms Under Asymmetric Information: An Experimental Investigation", authors: "Charles R Schnitzlein", type: ["lab"] },
  { year: 1996, journal: "JF", title: "Quotes, Prices, and Estimates in a Laboratory Market", authors: "Robert Bloomfield", type: ["lab"] },
  { year: 1996, journal: "RFS", title: "Collusion in Uniform-Price Auctions: Experimental Evidence and Implications for Treasury Auctions", authors: "Gautam Goswami, Thomas H Noe & Michael J Rebello", type: ["lab"] },
  { year: 1997, journal: "JF", title: "When It's Not the Only Game in Town: The Effect of Bilateral Search on the Quality of a Dealer Market", authors: "Christopher G Lamoureux & Charles R Schnitzlein", type: ["lab", "market"] },
  { year: 1997, journal: "RFS", title: "Unconditional and Conditional Takeover Offers: Experimental Evidence", authors: "Jayant R Kale & Thomas H Noe", type: ["lab"] },
  { year: 1999, journal: "RFS", title: "Quote Disclosure and Price Discovery in Multiple-Dealer Financial Markets", authors: "Mark D Flood, Ronald Huisman, Kees G Koedijk & Ronald J Mahieu", type: ["lab", "market"] },
  { year: 1999, journal: "RFS", title: "Cheap Talk, Fraud, and Adverse Selection in Financial Markets: Some Experimental Evidence", authors: "Robert Forsythe, Russell Lundholm & Thomas Rietz", type: ["lab", "market"] },
  { year: 2000, journal: "RFS", title: "The Opportunity for Conspiracy in Asset Markets Organized with Dealer Intermediaries", authors: "Timothy N Cason", type: ["lab", "market"] },
  { year: 2002, journal: "JFE", title: "Predicting the next step of a random walk: experimental evidence of regime-shifting beliefs", authors: "Robert Bloomfield & Jeffrey Hales", type: ["lab"] },
  { year: 2005, journal: "JF", title: "Do Professional Traders Exhibit Myopic Loss Aversion? An Experimental Analysis", authors: "Michael S Haigh & John A List", type: ["lab"] },
  { year: 2005, journal: "RFS", title: "Coordination of Expectations in Asset Pricing Experiments", authors: "Cars Hommes, Joep Sonnemans, Jan Tuinstra & Henk Van de Velden", type: ["lab"] },
  { year: 2006, journal: "JF", title: "The Effect of Short Selling on Bubbles and Crashes in Experimental Spot Asset Markets", authors: "Ernan Haruvy & Charles N Noussair", type: ["lab", "market"] },
  { year: 2006, journal: "RFS", title: "Competition and Cooperation in Divisible Good Auctions: An Experimental Examination", authors: "Orly Sade, Charles Schnitzlein & Jaime F Zender", type: ["lab"] },
  { year: 2007, journal: "JF", title: "Information Cascades: Evidence from a Field Experiment with Financial Market Professionals", authors: "Jonathan E Alevy, Michael S Haigh & John A List", type: ["lab"] },
  { year: 2009, journal: "RFS", title: "Distinguishing the Effect of Overconfidence from Rational Best-Response on Information Aggregation", authors: "Shimon Kogan", type: ["lab", "market"] },
  { year: 2009, journal: "RFS", title: "Margin Trading, Overpricing, and Synchronization Risk", authors: "Sanjeev Bhojraj, Robert J Bloomfield & William B Tayler", type: ["lab", "market"] },
  { year: 2009, journal: "RFS", title: "How Noise Trading Affects Markets: An Experimental Analysis", authors: "Robert Bloomfield, Maureen O’hara & Gideon Saar", type: ["lab", "market"] },
  { year: 2010, journal: "JF", title: "Exploring the Nature of “Trader Intuition”", authors: "Antoine J Bruguier, Steven R Quartz & Peter Bossaerts", type: ["lab", "market"] },
  { year: 2010, journal: "RFS", title: "Ambiguity in Asset Markets: Theory and Experiment", authors: "Peter Bossaerts, Paolo Ghirardato, Serena Guarnaschelli & William R Zame", type: ["lab", "market"] },
  { year: 2010, journal: "RFS", title: "Why Does the Law of One Price Fail? An Experiment on Index Mutual Funds", authors: "James J Choi, David Laibson & Brigitte C Madrian", type: ["lab"] },
  { year: 2011, journal: "JF", title: "Information Disclosure, Cognitive Biases, and Payday Borrowing", authors: "Marianne Bertrand & Adair Morse", type: ["field"] },
  { year: 2011, journal: "JF", title: "Prices or Knowledge? What Drives Demand for Financial Services in Emerging Markets?", authors: "Shawn Cole, Thomas Sampson & Bilal Zia", type: ["field"] },
  { year: 2013, journal: "JF", title: "The Effects of Stock Lending on Security Prices: An Experiment", authors: "Steven N Kaplan, Tobias J Moskowitz & Berk A Sensoy", type: ["lab", "field"] },
  { year: 2013, journal: "JF", title: "Trading Complex Assets", authors: "Bruce Ian Carlin, Shimon Kogan & Richard Lowery", type: ["lab"] },
  { year: 2013, journal: "JFE", title: "Managerial attitudes and corporate actions", authors: "John R Graham, Campbell R Harvey & Manju Puri", type: ["survey"] },
  { year: 2013, journal: "RFS", title: "’O Sole Mio: An Experimental Analysis of Weather and Risk Attitudes in Financial Decisions", authors: "Anna Bassi, Riccardo Colacito & Paolo Fulghieri", type: ["lab"] },
  { year: 2014, journal: "JF", title: "Using Neural Data to Test a Theory of Investor Behavior: An Application to Realization Utility", authors: "Cary Frydman, Nicholas Barberis, Colin Camerer & Peter Bossaerts et al.", type: ["lab", "market"] },
  { year: 2015, journal: "JF", title: "Incentivizing Calculated Risk‐Taking: Evidence from an Experiment with Commercial Bank Loan Officers", authors: "Shawn Cole, Martin Kanz & Leora Klapper", type: ["lab"] },
  { year: 2015, journal: "JF", title: "The Effect of Providing Peer Information on Retirement Savings Decisions", authors: "John Beshears, James J Choi, David Laibson & Brigitte C Madrian et al.", type: ["field"] },
  { year: 2015, journal: "JF", title: "Asymmetric learning from financial information", authors: "Camelia M Kuhnen", type: ["lab"] },
  { year: 2016, journal: "JF", title: "Looking for Someone to Blame: Delegation, Cognitive Dissonance, and the Disposition Effect", authors: "Tom Y Chang, David H Solomon & Mark M Westerfield", type: ["lab", "field"] },
  { year: 2016, journal: "JF", title: "“Lucas” in the Laboratory", authors: "Elena Asparouhova, Peter Bossaerts, Nilanjan Roy & William Zame", type: ["lab"] },
  { year: 2016, journal: "RFS", title: "Neural Evidence of Regret and Its Implications for Investor Behavior", authors: "Cary Frydman & Colin Camerer", type: ["lab"] },
  { year: 2017, journal: "JF", title: "Attracting Early‐Stage Investors: Evidence from a Randomized Field Experiment", authors: "Shai Bernstein, Arthur Korteweg & Kevin Laws", type: ["field"] },
  { year: 2017, journal: "JF", title: "Why Do Investors Hold Socially Responsible Mutual Funds?", authors: "Arno Riedl & Paul Smeets", type: ["lab", "field"] },
  { year: 2017, journal: "JFE", title: "Socioeconomic status and learning from financial information", authors: "Camelia M Kuhnen & Andrei C Miu", type: ["lab"] },
  { year: 2017, journal: "RFS", title: "How Does Risk Management Influence Production Decisions? Evidence from a Field Experiment", authors: "Shawn Cole & Gin{\\'e", type: ["field"] },
  { year: 2017, journal: "RFS", title: "Does Aggregated Returns Disclosure Increase Portfolio Risk Taking?", authors: "John Beshears, James J Choi, David Laibson & Brigitte C Madrian", type: ["lab"] },
  { year: 2017, journal: "RFS", title: "The Causal Effect of Stop-Loss and Take-Gain Orders on the Disposition Effect", authors: "Urs Fischbacher, Gerson Hoffmann & Simeon Schudy", type: ["lab"] },
  { year: 2018, journal: "JF", title: "What Makes a Good Trader? On the Role of Intuition and Reflection on Trader Performance", authors: "Brice Corgnet, Mark Desantis & David Porter", type: ["lab", "market"] },
  { year: 2018, journal: "JF", title: "An Experimental Study of Bond Market Pricing", authors: "Matthias Weber, John Duffy & Arthur Schram", type: ["lab", "market"] },
  { year: 2018, journal: "JF", title: "Rankings and Risk‐Taking in the Finance Industry", authors: "Michael Kirchler, Florian Lindner & Utz Weitzel", type: ["lab", "field"] },
  { year: 2018, journal: "JF", title: "Collateral Constraints and the Law of One Price: An Experiment", authors: "Marco Cipriani, Ana Fostel & Daniel Houser", type: ["lab", "market"] },
  { year: 2018, journal: "RFS", title: "Rolling Mental Accounts", authors: "Cary Frydman, Samuel M Hartzmark & David H Solomon", type: ["lab", "field"] },
  { year: 2018, journal: "RFS", title: "Can People Learn about ‘Black Swans’? Experimental Evidence", authors: "Elise Payzan-LeNestour", type: ["lab"] },
  { year: 2019, journal: "JF", title: "A Test of the Modigliani‐Miller Invariance Theorem and Arbitrage in Experimental Asset Markets", authors: "Gary Charness & Tibor Neugebauer", type: ["lab", "market"] },
  { year: 2019, journal: "JF", title: "Costly Information Acquisition, Social Networks, and Asset Prices: Experimental Evidence", authors: "Edward Halim, Yohanes E Riyanto & Nilanjan Roy", type: ["lab", "market"] },
  { year: 2019, journal: "JF", title: "Thinking about Prices versus Thinking about Returns in Financial Markets", authors: "Markus Glaser, Zwetelina Iliewa & Martin Weber", type: ["lab"] },
  { year: 2019, journal: "RFS", title: "Low Interest Rates and Risk-Taking: Evidence from Individual Investment Decisions", authors: "Chen Lian, Yueran Ma & Carmen Wang", type: ["lab"] },
  { year: 2019, journal: "RFS", title: "Unleashing Animal Spirits: Self-Control and Overpricing in Experimental Asset Markets", authors: "Martin G Kocher, Konstantin E Lucks & David Schindler", type: ["lab", "market"] },
  { year: 2020, journal: "RFS", title: "Financial Illiteracy and Pension Contributions: A Field Experiment on Compound Interest in China", authors: "Changcheng Song", type: ["field"] },
  { year: 2020, journal: "RFS", title: "Bubbles and Financial Professionals", authors: "Utz Weitzel, Christoph Huber & J{\\\"u Huber", type: ["lab", "market"] },
  { year: 2020, journal: "RFS", title: "Overcoming Discount Window Stigma: An Experimental Investigation", authors: "Olivier Armantier & Charles A Holt", type: ["lab"] },
  { year: 2021, journal: "JF", title: "The Perception of Dependence, Investment Decisions, and Stock Prices", authors: "Michael Ungeheuer & Martin Weber", type: ["lab", "field"] },
  { year: 2021, journal: "JFE", title: "Testing the effectiveness of consumer financial disclosure: Experimental evidence from savings accounts", authors: "Paul Adams, Stefan Hunt, Christopher Palmer & Redis Zaliauskas", type: ["field"] },
  { year: 2021, journal: "RFS", title: "Side Effects of Nudging: Evidence from a Randomized Intervention in the Credit Card Market", authors: "Paolina C Medina", type: ["field"] },
  { year: 2021, journal: "RFS", title: "How Much Information Is Incorporated into Financial Asset Prices? Experimental Evidence", authors: "Lionel Page & Christoph Siemroth", type: ["lab", "market"] },
  { year: 2021, journal: "RFS", title: "Experience Does Not Eliminate Bubbles: Experimental Evidence", authors: "Kop{\\'a", type: ["lab", "market"] },
  { year: 2022, journal: "JF", title: "Increasing Enrollment in Income‐Driven Student Loan Repayment Plans: Evidence from the Navient Field Experiment", authors: "Holger Mueller & Constantine Yannelis", type: ["field"] },
  { year: 2022, journal: "JFE", title: "Outlier blindness: A neurobiological foundation for neglect of financial risk", authors: "Elise Payzan-LeNestour & Michael Woodford", type: ["lab"] },
  { year: 2022, journal: "JFE", title: "Stock return ignorance", authors: "Yulia Merkoulova & Chris Veld", type: ["survey"] },
  { year: 2022, journal: "JFE", title: "Measuring the welfare cost of asymmetric information in consumer credit markets", authors: "Anthony A DeFusco, Huan Tang & Constantine Yannelis", type: ["lab"] },
  { year: 2022, journal: "RFS", title: "Efficiency of Dynamic Portfolio Choices: An Experiment", authors: "Jacopo Magnani, Jean Paul Rabanal, Olga A Rud & Yabin Wang", type: ["lab"] },
  { year: 2022, journal: "RFS", title: "Biased by Choice: How Financial Constraints Can Reduce Financial Mistakes", authors: "Rawley Z Heimer & Alex Imas", type: ["lab", "field"] },
  { year: 2022, journal: "RFS", title: "A Fistful of Dollars: Financial Incentives, Peer Information, and Retirement Savings", authors: "Rob Bauer, Inka Eberhardt & Paul Smeets", type: ["field"] },
  { year: 2022, journal: "RFS", title: "Decision Weights for Experimental Asset Prices Based on Visual Salience", authors: "Devdeepta Bose, Henning Cordes, Sven Nolte & Judith Christiane Schneider et al.", type: ["lab"] },
  { year: 2023, journal: "JFE", title: "When can the market identify old news?", authors: "Anastassia Fedyk & James Hodson", type: ["lab"] },
  { year: null, journal: "JFE", title: "Associative Memory, Beliefs and Market Interactions", authors: "Benjamin Enke, Frederik Schwerter & Florian Zimmermann", type: ["lab", "market"], forthcoming: true },
  { year: null, journal: "JF", title: "Insensitive Investors", authors: "Constantin Charles, Cary Frydman & Mete Kilic", type: ["lab"], forthcoming: true }
];


let currentFilter = "all", currentSearch = "";

function renderTable() {
  var tbody = document.getElementById("paper-tbody");
  var countEl = document.getElementById("paper-count");
  var table = document.getElementById("paper-table");

  // Hide table and show prompt if no search query
  if (!currentSearch.trim()) {
    table.style.display = "none";
    countEl.textContent = "Type above to search " + papers.length + " papers.";
    return;
  }

  table.style.display = "";
  var filtered = papers.filter(function(p) {
    var mf = currentFilter === "all" || p.journal === currentFilter;
    var q  = currentSearch.toLowerCase();
    var ms = p.title.toLowerCase().includes(q)
              || p.authors.toLowerCase().includes(q)
              || p.type.some(function(t){ return t.includes(q); });
    return mf && ms;
  });
  filtered.sort(function(a,b){ return (b.year||9999)-(a.year||9999); });
  tbody.innerHTML = filtered.map(function(p) {
    var jc   = p.journal.toLowerCase();
    var tags = p.type.map(function(t){ return '<span class="exp-tag">'+t+'</span>'; }).join("");
    var yr   = p.year || "FC";
    return '<tr><td>'+yr+'</td>'
      +'<td><span class="badge badge-'+jc+'">'+p.journal+'</span></td>'
      +'<td><div class="paper-title">'+p.title+'</div>'
      +'<div class="paper-authors">'+p.authors+'</div></td>'
      +'<td>'+tags+'</td></tr>';
  }).join("");
  countEl.textContent = filtered.length + " of " + papers.length + " papers";
}

function filterTable(btn, filter) {
  document.querySelectorAll(".filter-btn").forEach(function(b){ b.classList.remove("active"); });
  btn.classList.add("active");
  currentFilter = filter;
  renderTable();
}

function searchTable(val) { currentSearch = val; renderTable(); }

function updateStats() {
  document.getElementById("stat-jf").textContent  = papers.filter(function(p){ return p.journal==="JF"; }).length;
  document.getElementById("stat-jfe").textContent = papers.filter(function(p){ return p.journal==="JFE"; }).length;
  document.getElementById("stat-rfs").textContent = papers.filter(function(p){ return p.journal==="RFS"; }).length;
}

renderTable();
updateStats();
