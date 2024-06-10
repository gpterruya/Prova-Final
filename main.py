# Importa o FastAPI
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
# Importa o SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
#  Importa o os
import os
import datetime


# Instancia o FastAPI
app = FastAPI()

SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///./prova.db')

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Cria uma sessão para o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# Cria uma classe que herda do declarative_base
Base = declarative_base()

# Cria uma classe User que herda da classe Base
class Department(Base):
	# Define o nome da tabela
	__tablename__ = "department"
	# Define o id como uma coluna do tipo Integer
	id = Column(Integer, primary_key=True, index=True)
	# Define o nome como uma coluna do tipo String
	name = Column(String)
	# Define a região como uma coluna do tipo String
	region = Column(String)
	employee = relationship("Employee", back_populates="department")

class Employee(Base):
	__tablename__ = "employee"
	id = Column(Integer, primary_key=True, index=True)
	department_id = Column(Integer, ForeignKey('department.id'))
	name = Column(String)
	birthday = Column(String)
	salary = Column(Float, nullable=True)
	job = Column(String)
	department = relationship("Department", back_populates="employee")
	jobhistory = relationship("JobHistory", back_populates="employee")

class JobHistory(Base):
	__tablename__ = "jobhistory"
	id = Column(Integer, primary_key=True, index=True)
	employee_id = Column(Integer, ForeignKey('employee.id'))
	startdate = Column(String)
	enddate = Column(String)
	salary = Column(Float, nullable=True)
	job = Column(String)
	title = Column(String)
	employee = relationship("Employee", back_populates="jobhistory")

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)


# Departamento
# Cria uma rota de GET com o path "/author"
@app.get("/department")
def read_departments():
	# Cria uma variável users que recebe todos os usuários
	departments = session.query(Department).all()
	# Cria uma lista vazia
	departments_list = []
	# Para cada usuário em users
	for department in departments:
		# Cria um dicionário com o id, nome e região do usuário
		departments_dict = {"id": department.id, "name": department.name, "region": department.region}
		# Adiciona o dicionário na lista
		departments_list.append(departments_dict)
	# Retorna um JSON com a lista de usuários
	return JSONResponse(content=departments_list)

# Cria uma rota de GET com o path "/users/{user_id}"
@app.get("/department/{department_id}")
def read_department(department_id: int):
	# Cria uma variável user que recebe o usuário com o id fornecido
	department = session.query(Department).filter(Department.id == department_id).first()
	if not department:
		raise HTTPException(status_code=404, detail="Department not found")
	employees = session.query(Employee).filter(Employee.department_id == department_id).all()
	employees_list = []
	for employee in employees:
		jobhistory = session.query(JobHistory).filter(JobHistory.employee_id == employee.id).all()
		jobhistory_list = [{"id": jobhistory.id, "title": jobhistory.title, "startdate": jobhistory.startdate, "enddate": jobhistory.enddate, "salary": jobhistory.salary, "job": jobhistory.job} for jobhistory in jobhistory]
		employee_dict = {"id": employee.id, "name": employee.name, "birthday": employee.birthday, "salary": employee.salary, "job": employee.job, "jobhistory": jobhistory_list}
		employees_list.append(employee_dict)
	# Cria o dicionário do departamento
	department_dict = {"id": department.id, "name": department.name, "region": department.region, "employees": employees_list}
	return JSONResponse(content=department_dict)
	
# Cria uma rota de POST com o path "/department"
@app.post("/department")
def create_department(name: str, region: str):
	# Cria um objeto da classe Department
	department = Department(name=name, region=region)
	# Adiciona o usuário ao banco de dados
	session.add(department)
	# Salva as alterações no banco de dados
	session.commit()
	# Retorna um JSON com o id, nome e email do usuário
	return JSONResponse(content={"id": department.id, "name": department.name, "region": department.region})

# Cria uma rota de PUT com o path "/department/{department_id}"
@app.put("/departmnet/{department_id}")
def update_department(department_id: int, name: str, region: str):
	# Cria uma variável user que recebe o usuário com o id fornecido
	department = session.query(Department).filter(Department.id == department_id).first()
	# Atualiza o nome do usuário
	department.name = name
	# Atualiza o email do usuário
	department.region = region
	# Salva as alterações no banco de dados
	session.commit()
	# Retorna um JSON com o id, nome e email do usuário
	return JSONResponse(content={"id": department.id, "name": department.name, "region": department.region})

# Cria uma rota de DELETE com o path "/department/{department_id}"
@app.delete("/department/{department_id}")
def delete_department(department_id: int):
	# Cria uma variável user que recebe o usuário com o id fornecido
	department = session.query(Department).filter(Department.id == department_id).first()
	# Remove o usuário do banco de dados
	session.delete(department)
	# Salva as alterações no banco de dados
	session.commit()
	# Retorna um JSON com o id, nome e email do usuário
	return JSONResponse(content={"id": department.id, "name": department.name, "region": department.region})

# Employee

# Cria uma rota de GET com o path "/employees"
@app.get("/employee")
def read_employees():
	# Cria uma variável users que recebe todos os usuários
	employees = session.query(Employee).all()
	# Cria uma lista vazia
	employees_list = []
	# Para cada usuário em users
	for employee in employees:
		# Cria um dicionário com o id, nome e região do usuário
		employees_dict = {"id": employee.id, "name": employee.name, "birthday": employee.birthday, "salary": employee.salary, "job": employee.job}
		# Adiciona o dicionário na lista
		employees_list.append(employees_dict)
	# Retorna um JSON com a lista de usuários
	return JSONResponse(content=employees_list)

# Cria uma rota de GET com o path "/users/{user_id}"
@app.get("/employee/{employee_id}")
def read_employee(employee_id: int):
	# Cria uma variável user que recebe o usuário com o id fornecido
	employee = session.query(Employee).filter(Employee.id == employee_id).first()
	if not employee:
		raise HTTPException(status_code=404, detail="Employee not found")
	jobhistory = session.query(JobHistory).filter(JobHistory.employee_id == employee_id).all()
	jobhistory_list = [{"id": jobhistory.id, "title": jobhistory.title, "startdate": jobhistory.startdate, "enddate": jobhistory.enddate, "salary": jobhistory.salary, "job": jobhistory.job} for jobhistory in jobhistory]
	# Cria o dicionário do funcionário
	employee_dict = {"id": employee.id, "name": employee.name, "birthday": employee.birthday, "salary": employee.salary, "job": employee.job, "jobhistory": jobhistory_list}
	return JSONResponse(content=employee_dict)

# Cria uma rota de POST com o path "/employee"
@app.post("/employee")
def create_employee(name: str, birthday: str, salary: float, job: str, department_id: int):
	# Cria um objeto da classe Employee
	employee = Employee(name=name, birthday=birthday, salary=salary, job=job, department_id=department_id)
	# Adiciona o usuário ao banco de dados
	session.add(employee)
	# Salva as alterações no banco de dados
	session.commit()
	# Retorna um JSON com o id, nome e email do usuário
	return JSONResponse(content={"id": employee.id, "name": employee.name, "birthday": employee.birthday, "salary": employee.salary, "job": employee.job, "department_id": employee.department_id})

# Cria uma rota de PUT com o path "/department/{department_id}"
@app.put("/employee/{employee_id}")
def update_employee(employee_id: int, name: str, birthday: str, salary: float, job: str, department_id: int):
	# Cria uma variável user que recebe o usuário com o id fornecido
	employee = session.query(Employee).filter(Employee.id == employee_id).first()
	# Atualiza o nome do usuário
	employee.name = name
	# Atualiza a data de aniversário do usuário
	employee.birthday = birthday
	# Atualiza o salário do usuário
	employee.salary = salary
	# Atualiza o cargo do usuário
	employee.job = job
	# Atualiza o departamento do usuário
	employee.department_id = department_id
	# Salva as alterações no banco de dados
	session.commit()
	# Retorna um JSON com o id, nome e email do usuário
	return JSONResponse(content={"id": employee.id, "name": employee.name, "birthday": employee.birthday, "salary": employee.salary, "job": employee.job, "department": employee.department_id})

# Cria uma rota de DELETE com o path "/department/{department_id}"
@app.delete("/employee/{employee_id}")
def delete_employee(employee_id: int):
	# Cria uma variável user que recebe o usuário com o id fornecido
	employee = session.query(Employee).filter(Employee.id == employee_id).first()
	# Remove o usuário do banco de dados
	session.delete(employee)
	# Salva as alterações no banco de dados
	session.commit()
	# Retorna um JSON com o id, nome e email do usuário
	return JSONResponse(content={"id": employee.id, "name": employee.name, "birthday": employee.birthday, "salary": employee.salary, "job": employee.job, "department": employee.department_id})

# JobHistory

# Cria uma rota de GET com o path "/jobhistory"
@app.get("/jobhistory")
def read_jobhistory(employee_id: int):
	employee = session.query(Employee).filter(Employee.id == employee_id).first()
	if not employee:
		session.close()
		raise HTTPException(status_code=404, detail="Employee not found")
	# Cria uma variável users que recebe todos os usuários
	jobhistory = session.query(JobHistory).all()
	jobhistory_list = [{"id": jobhistory.id, "title": jobhistory.title, "startdate": jobhistory.startdate, "enddate": jobhistory.enddate, "salary": jobhistory.salary, "job": jobhistory.job} for jobhistory in jobhistory]
	# Cria um dicionário com o id, nome e região do usuário
	employee_dict = {"id": employee.id, "birthday": employee.birthday, "salary": employee.salary, "job": employee.job, "jobhistory": jobhistory_list}
	# Retorna um JSON com a lista de usuários
	return JSONResponse(content=employee_dict)

# Cria uma rota de POST com o path "/jobhistory"
@app.post("/jobhistory")
def create_jobhistory(employee_id: int, startdate: str, enddate: str, salary: float, job: str, title: str):
	# Cria um objeto da classe Employee
	jobhistory = JobHistory(title=title, startdate=startdate, enddate=enddate, salary=salary, job=job, employee_id=employee_id)
	# Adiciona o usuário ao banco de dados
	session.add(jobhistory)
	# Salva as alterações no banco de dados
	session.commit()
	# Retorna um JSON com o id, nome e email do usuário
	return JSONResponse(content={"id": jobhistory.employee_id, "title": jobhistory.title, "startdate": jobhistory.startdate, "enddate": jobhistory.enddate, "salary": jobhistory.salary, "job": jobhistory.job})

# Cria uma rota de PUT com o path "/department/{department_id}"
@app.put("/jobhistory/{jobhistory_id}")
def update_jobhistory(employee_id: int, jobhistory_id: int, title: str, startdate: str, enddate: str, salary: float, job: str):
	jobhistory = session.query(JobHistory).filter(JobHistory.id == jobhistory_id).first()
	if not jobhistory:
		session.close()
		raise HTTPException(status_code=404, detail="JobHistory not found")
	jobhistory.employee_id = employee_id
	jobhistory_id = jobhistory_id
	jobhistory.title = title
	jobhistory.startdate = startdate
	jobhistory.enddate = enddate
	jobhistory.salary = salary
	jobhistory.job = job
	session.commit()

	# Retorna um JSON com o id, nome e email do usuário
	return JSONResponse(content={"employee_id": jobhistory.employee_id, "jobhistory_id": jobhistory.id, "title": jobhistory.title, "startdate": jobhistory.startdate,"enddate": jobhistory.enddate, "job": jobhistory.job, "salary": jobhistory.salary})

# Cria uma rota de DELETE com o path "/department/{department_id}"
@app.delete("/jobhistory/{jobhistory_id}")
def delete_jobhistory(employee_id: int, jobhistory_id: int):
	# Cria uma variável user que recebe o usuário com o id fornecido
	jobhistory = session.query(JobHistory).filter(JobHistory.id == jobhistory_id).first()
	# Remove o usuário do banco de dados
	session.delete(jobhistory)
	# Salva as alterações no banco de dados
	session.commit()
	# Retorna um JSON com o id, nome e email do usuário
	return JSONResponse(content={"employee_id": jobhistory.employee_id, "jobhistory_id": jobhistory_id, "title": jobhistory.title, "job": jobhistory.job})