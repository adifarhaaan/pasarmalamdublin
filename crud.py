from app import db,Vendor,app

with app.app_context():
	all_vendor = Vendor.query.all()
	print(all_vendor)


	vendor_one = Vendor.query.get(1)
	print(vendor_one.name)


	vendor_ciliemas = Vendor.query.filter_by(name='goldcili')
	print(vendor_ciliemas.all())



	