from main import Business
from main import business_id_name_dict
# 存放id - name


ids = "0-3kCit8mt8cCjiQXDyg8w"
business = Business(ids, business_id_name_dict.get(ids))
fianl_result=business.extract_aspects().aspect_based_summary()
print(fianl_result)