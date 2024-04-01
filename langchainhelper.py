#!/usr/bin/env python
# coding: utf-8

# In[1]:

def get_few_shot_db_chain():
  from langchain.llms import GooglePalm
  from langchain.chains import ConversationChain
  from langchain.memory import ConversationBufferMemory
  
  
  # In[2]:
  
  
  key = "AIzaSyCZLRSi1VOBHMHiv1tXu85oSNmzxP4LFM0"
  
  
  # In[3]:
  
  
  llm= GooglePalm(google_api_key = key, temperature = 0 )
  
  
  # In[4]:
  
  
  llm("write about samosa")
  
  
  # In[4]:
  
  
  from langchain.utilities import SQLDatabase
  db_user="root"
  db_password = "root"
  db_host= "localhost"
  db_name ="atliq_tshirts"
  db =SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",
                                sample_rows_in_table_info=3)
  print(db.table_info)
  
  
  # In[5]:
  
  
  from langchain_experimental.sql import SQLDatabaseChain
  
  db_chain = SQLDatabaseChain.from_llm(llm,db, verbose = True)
  
  
  # In[36]:
  
  
  # Create the ConversationBufferMemory
  memory2 = ConversationBufferMemory(memory_key="history") 
  
  # Create the ConversationChain, using memory 
  conversation_chain = ConversationChain(llm=db_chain, memory=memory) 
  
  
  # In[7]:
  
  
  # db_chain("how many tshirts are there")
  
  
  # In[8]:
  
  
  # db_chain.run("what is the total quantity of Nike tshirts")
  
  
  # In[9]:
  
  
  # qn2=db_chain.run("What is the total cost of all nike extra small black shirts")
  
  
  # In[10]:
  
  
  qn2= db_chain.run("""SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from
  (select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where brand = 'Nike' and size="L"
  group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id
   """)
  
  
  # In[11]:
  
  
  # SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS'
  
  
  # In[12]:
  
  
  few_shots = [
      {'Question': "I want to order a Nike extra small shirt ",
       'SQLQuery': "INSERT INTO order_status (order_name, order_status) VALUES ('Nike', 'Ordered');",  # No query needed for empty user input
       'SQLResult': "result of the sql query",  # No result for empty query
       'Answer': "Order placed!. Thank you for your order. You order will be delivered in 5 days/ Would you like to order anything else?"},
       {'Question': "I want to order a benx extra small shirt ",
       'SQLQuery': "INSERT INTO order_status (order_name, order_status) VALUES ('benx', 'Ordered');",  # No query needed for empty user input
       'SQLResult': "result of the sql query",  # No result for empty query
       'Answer': "we dont have benx shirts. would you like to order nike instead"},
      {'Question': "My order is not delivered yet, order id is 11",
       'SQLQuery': "select order_status from order_status where order_id = 11;",  # No query needed for empty user input
       'SQLResult': "result of the sql query",  # No result for empty query
       'Answer': "We are sorry that your order is delayed, Please wait for 2 more days. If your order is not delivered , we will process your refund."},
      # User ends conversation and various other interactions
      {'Question': "No, I don't want to purchase anything",
       
       'Answer': "I'm sorry to hear that. Is there anything else I can assist you with?"},
      {'Question': "oh NO!",
       
       'Answer': "I am so sorry you are disappointed, If you need anything else , I am so happy to assist you!"},
     # Continued from previous response...
      {'Question': "I DONT LIKE THIS!!!",
       'SQLQuery': "select * from user_emotions",
       'SQLResult': "result of the sql query",  # No SQL result shown to user
       'Answer': "Please be calm sir. We are trying our best to assist you today. Please tell me if you need anything!"},
      {'Question': " ",
       'SQLQuery': "select * from user_emotions and previous_conversations",
       'SQLResult': "result of the sql query",  # No SQL result shown to user
       'Answer': "Thanks for checking out our inventory! Would you like to sign up for our newsletter to receive updates on new arrivals and special offers? No problem at all! Feel free to come back anytime to explore our selection."},
      {'Question': "No, I'm just browsing for now, thanks.",
       'SQLQuery': "select * from user_emotions",
       'SQLResult': "result of the sql query",  # No SQL result shown to user
       'Answer': "Sure thing! Feel free to explore our products at your own pace. If you have any questions or need assistance, don't hesitate to ask."},
      {'Question': "I'm not interested in purchasing at the moment.",
       'SQLQuery': "select * from user_emotions ",
       'SQLResult': "result of the sql query",  # No SQL result shown to user
       'Answer': "That's perfectly fine! Let me know if you have any questions about our products or if there's anything else I can assist you with."},
      {'Question': "I'm just checking out the options.",
       'SQLQuery': "select * from user_emotions ",
       'SQLResult': "result of the sql query",  # No SQL result shown to user
       'Answer': "No problem! Take your time exploring our options. If you need any help or have questions along the way, don't hesitate to ask."},
       {'Question': "I'll come back later if I decide to buy something.",
       'SQLQuery': "select * from user_emotions ",
       'SQLResult': "result of the sql query",  # No SQL result shown to user
       'Answer': "Sounds good! Remember, I'm here to assist you whenever you're ready. Don't hesitate to reach out if you need anything in the future."},
      {'Question': "I'm not looking to make a purchase right now.",
       'SQLQuery': "select * from user_emotions",
       'SQLResult': "result of the sql query",  # No SQL result shown to user
       'Answer': "No problem at all! If you ever change your mind or have questions about our products, feel free to reach out. I'm here to help whenever you need."},
      {'Question': "Find the number of Nike XS white t-shirts in stock",
       'SQLQuery': "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS'",
       'SQLResult': "result of sql query",  # No SQL result shown to user
       'Answer': "There are 10 Nike XS size white color t-shirts. Do you have any other questions about our inventory?"},
      {'Question': "Calculate the total price of all S-size t-shirts",
       'SQLQuery':"SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'S'",
       'SQLResult': "result of sql query",  # No SQL result shown to user
       'Answer': "The total price of all S-size t-shirts is 23723. Would you like to see a breakdown of this by color or size?"},
      
      
      {'Question': "How many white Levi's shirts do you have?",
       'SQLQuery': "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Levi' AND color = 'White'",
       'SQLResult': "result of sql query",  # No SQL result shown to user
       'Answer': "There are a total of 285 white Levi's shirts in our inventory. Are you interested in other colors or brands?"},
      {'Question': "Calculate the total sales amount generated if we sell all large Nike t-shirts today after applying discounts",
       'SQLQuery': """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from
  (select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where brand = 'Nike' and size="L"
  group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id
   """,
       'SQLResult': "result of sql query",  # No SQL result shown to user
       'Answer': "The total sales amount generated from selling all large Nike t-shirts today after discounts is 341.00. Would you like to know about sales amounts for other sizes or brands?"},
  
      
  ]
  
  
  # In[13]:
  
  
  from langchain.embeddings import HuggingFaceEmbeddings
  from langchain_community.embeddings.sentence_transformer import (
      SentenceTransformerEmbeddings,
  )
  embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
  
  
  # In[14]:
  
  
  to_vectorize = [" ".join(example.values()) for example in few_shots]
  
  
  # In[15]:
  
  
  # pip install -U langchain chromadb
  
  
  # In[16]:
  
  
  to_vectorize
  
  
  # In[17]:
  
  
  # chromadb --version
  
  
  # In[18]:
  
  
  from langchain.vectorstores import Chroma
  from langchain.vectorstores import FAISS
  # Create a Chroma vectorstore with your embeddings and data
  
  
  # In[19]:
  
  
  vectorstore = FAISS.from_texts(to_vectorize, embeddings, metadatas=few_shots)
  
  
  # In[20]:
  
  
  # vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=few_shots)
  
  
  # In[21]:
  
  
  from langchain.prompts import SemanticSimilarityExampleSelector
  example_selector = SemanticSimilarityExampleSelector(
          vectorstore=vectorstore,
          k=2,
      )
  example_selector.select_examples({"Question":"How many t-shirts do we have left for Nike in XS size and white color?"})
  
  
  # In[22]:
  
  
  from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
  
  
  # In[23]:
  
  
  _mysql_prompt
  
  
  # In[24]:
  
  
  # mysql_prompt = "You are a MySQL expert. Given an input question, first look at the previous_conversations table and retrieve the most recent 10 conversations using: SELECT question, answer FROM previous_conversations ORDER BY created_at DESC LIMIT 10; and Try to answer it generally if possible and only create a syntactically correct MySQL query to run if necessary, then look at the results of the query and return the answer to the input question. If the user doesn't ask anything related to the database information, Do not run any query and try to answer based on previous_conversation table. Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database. Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers. Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table. Pay attention to use CURDATE() function to get the current date, if the question involves 'today'. Use the following format: Question: Question here, SQLQuery(only if necessary, otherwise dont run the query): SQL Query to run only if necessary for the question, SQLResult: Result of the SQLQuery only if you run the query, Answer: Final answer here with proper sentence formation, **Manage Conversation History:** After answering the user's question, insert the current question and answer into the previous_conversations table using: INSERT INTO previous_conversations (question, answer) VALUES (%s, %s); If the number of conversations in the table reaches 10 (check using SELECT COUNT(*) FROM previous_conversations), delete the oldest conversation (the first row) using: DELETE FROM previous_conversations ORDER BY created_at ASC LIMIT 1; Always store last 10 questions and answers in a table called previous_conversations and for every 11th question delete the first question and store latest question and answer at last row. After that ask a follow-up question for the user as a courtesy. "
  # mysql_prompt=    [" ".join(example.values()) for example in mysql_prompt]
  # mysql_prompt = 'You are a MySQL expert. Given an input question, First look at the previous conversations using memory  and based on that understand previous conversation but do not return them.\n if the question is about inventory first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.\nUnless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database. If question is not about inventory based on the user emotion just run the query "select * from user_emotions"  and answer appropriatley based on previous_conversations table and user_emotions using timestamp. \nNever query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.\nPay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist.Also pay attention as if user is asking anything related to inventory, Only run the query if the question is about inventory. If user is not asking about inventory do not run any sql queryand directly answer based on previous_conversations table using timestamp. Also, pay attention to which column is in which table.\nPay attention to use CURDATE() function to get the current date, if the question involves "today".\n\nUse the following format if the question is about inventory:\n\nQuestion: Question here\nSQLQuery:SQL Query to run\nSQLResult:  Result of the SQLQuery\nAnswer: Final answer here\n\n.  At the end of each conversations add question and answer in previous conversation table using following query INSERT INTO previous_conversations (question, answer) VALUES (**user question**, **answer**); at the end ask a follow up question. \n if the user is shocked, angry, confused, or in any other emotions, do not run sql query amd answer appropriately according to his/her emotions'
  mysql_prompt = "You are a MySQL expert. Given an input question, first look at the previous conversations using memory and based on that understand the previous conversation but do not return them. Conversation History: {history} If the question is about inventory, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question. Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database. If question is not about inventory based on the user emotion just run the query \"select * from user_emotions\" and answer appropriatley based on previous_conversations table and user_emotions using timestamp. Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers. Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also pay attention as if user is asking anything related to inventory, Only run the query if the question is about inventory. If user is not asking about inventory do not run any sql query and directly answer based on previous_conversations table using timestamp. Also, pay attention to which column is in which table. Pay attention to use CURDATE() function to get the current date, if the question involves \"today\". Use the following format if the question is about inventory: Question: Question here SQLQuery: SQL Query to run SQLResult: Result of the SQLQuery Answer: Final answer here. At the end of each conversations add question and answer in previous conversation table using following query INSERT INTO previous_conversations (question, answer) VALUES (**user question**, **answer**); at the end ask a follow up question. if the user is shocked, angry, confused, or in any other emotions, do not run sql query amd answer appropriately according to his/her emotions" 
  
  
  
  print(mysql_prompt)
  print(PROMPT_SUFFIX)
  
  
  # In[25]:
  
  
  from langchain.prompts.prompt import PromptTemplate
  
  
  # In[26]:
  
  
  example_prompt = PromptTemplate(
         input_variables=["Question", "Answer",],
         template="\nQuestion: {Question}\nAnswer: {Answer}",
     )
  
  
  # In[27]:
  
  
  from langchain.prompts import FewShotPromptTemplate
  
  
  # In[28]:
  
  
  few_shot_prompt = FewShotPromptTemplate(
      example_selector=example_selector,
      example_prompt=example_prompt,
      prefix=mysql_prompt,
      suffix=PROMPT_SUFFIX,
      input_variables=["input", "table_info", "top_k", "history"], # add 'history' here
  )
  
  
  # In[37]:
  
  
  memory = ConversationBufferMemory(memory_key="history") 
  chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, prompt=few_shot_prompt, memory = memory)
  return chain

