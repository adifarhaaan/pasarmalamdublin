from app import app,db,Vendor

with app.app_context():

	####db.create_all()


	kedaisatu = Vendor('wak doyok','ayam merah',3,"dublin 15")
	kedaidua = Vendor('kedai kuih','karipap',6,"dublin 1")

	print(kedaisatu.id)
	print(kedaidua.id)

	db.session.add_all([kedaisatu,kedaidua])

	db.session.commit()

	print(kedaisatu.id)
	print(kedaidua.id)