from datetime import date

today = date.today()

# dd/mm/YY
d1 = today.strftime("%d")
print(d1)
m1 = today.strftime("%m")
print(m1)
a1 = today.strftime("%y")
print(a1)

#18220609

hst_name = f"18{a1}{m1}{d1}.hst"

print(hst_name)