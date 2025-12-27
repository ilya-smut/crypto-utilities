import utilities

print(utilities.a_mod_p(-7, 8))

print(utilities.get_mod_inverse_euclid(8, 359334085968622831041960188598043661065388726959079837))
print(utilities.get_mod_inverse_fermat(8, 359334085968622831041960188598043661065388726959079837))


f1 = utilities.a_mod_p(8**55, 19)
f2 = utilities.fast_powering(8, 55, 19)

print(f1, f2)