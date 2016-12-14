import numpy as np
#from round_to_significance import *

debug = True
debug = False

def round_to_significance_sign(var):
	if (var<0):
		return -1
	elif (var>0):
		return 1
	return 0


def round_to_significance_get_base(var):
	if debug: print("round_to_significance_get_base called with", var)
	base_n = 0
	if var==0: return 1
	
	if var >= 10:
		while (var != 0):
			base_n += 1
			var = int(var / 10)
		return base_n-1
	
	if var <= 1:
		while (var < 1):
			base_n -= 1
			var *= 10
		return base_n-1
	
	return 0
    
    
def round_to_significance_get_significant_digits(var, error):
	if (debug): print("round_to_significance_get_significant_digits called with" , var, error)
	if ( error == 0 or error == None ) :
		return 0
	
	multiplied = 0
	while ( error>1 ):
		var /= 10
		error /= 10
		multiplied -= 1
	while (error < 1):
		var *= 10
		error *= 10
		multiplied += 1
	if debug: print("multiplied:", multiplied)
		
	error_base = round_to_significance_get_base(error)
	if (debug): print("e_base", error_base)
	var_base = round_to_significance_get_base(var)
	if (debug): print("var_base", var_base)

	significant_digits = error_base + multiplied + 1
	if (debug): print("significant_digits", significant_digits)
	
	# this step is needed to make (15, 10)
	# to 15 +- 10 instad of 20 +- 10
	if (error_base == var_base):
		if multiplied < 0:
			significant_digits -= 1
			if (debug): print("value and error have same order of magnitude -> significant_digits reduced by one")
	
	return significant_digits
	
	
def round_to_significance_round(var, digits):
	if (debug): print("round_to_significance_round called with" , var, digits)
	var_ret = float(var)
	
	if digits < 0:
		var_ret = round(var_ret, digits)
		var_ret = str(("{0:.0f}").format(var_ret))
	else:
		var_ret = str(("{0:."+str(digits)+"f}").format(round(var_ret, digits)))
	
	return var_ret
        

def round_to_significance(var, error=None, use_exponent=None):
	if debug: print("round_to_significance called with:", var, error, use_exponent)
	var_sgn = round_to_significance_sign(var)
	if error == None:
		return (str(var), None, 0, 0)
	if ( np.isinf(error) ):
		return (str(var), r'\infty', 0, 0)
	if( np.isnan(error) ):
		return (str(var), r'NaN', 0, 0)
	
	var = abs(var)
	error = abs(error)
	
	if debug: print("getting digits")
	digits = round_to_significance_get_significant_digits(var, error)
	if debug: print("digits (of error)=", digits)
	
	exponent = 0
	base = round_to_significance_get_base(var)
	error_base = round_to_significance_get_base(error)
	if debug: print("base=", base)
	if debug: print("error_base=", error_base)
	if use_exponent != None:
		if debug: print("using exponent", use_exponent)
		if use_exponent > 0:
			for i in range(0, use_exponent):
				var /= 10
				error /= 10
				digits += 1
				exponent += 1
		else:
			for i in range(use_exponent, 0):
				var *= 10
				error *= 10
				digits -= 1
				exponent -= 1
	elif error_base<-3:
		while round_to_significance_get_base(error)<1:
			var *= 10
			error *= 10
			digits -= 1
			exponent -= 1
	elif error_base>3:
		while round_to_significance_get_base(error)>1:
			var /= 10
			error /= 10
			digits += 1
			exponent += 1
	
	if round(var, digits-1)==0:
		var_ret = round_to_significance_round(0, digits)
	else:
		var_ret = round_to_significance_round(var_sgn*round(var, digits-1), digits)
	
	error_ret = round_to_significance_round(error, digits)
	
	if debug: print("round_to_significance returning:", var_ret, error_ret, exponent, '\n')
	return (var_ret, error_ret, exponent, digits)
	
	
    
    #~ if (digits!=None):
        #~ var = round(var, digits)
        #~ error = round(error, digits)
    #~ if(debug): print("digits=", digits)
    
    #~ multiplied = 0
    #~ # satisfy the wanted digits if needed
    #~ while (var != 0 and digits!=None and var < (10**digits)):
        #~ multiplied += 1
        #~ error *= 10
        #~ var *= 10
    #~ if(debug): print("satisfying digits=", var, error)
        
    #~ # also scale if the error is 0
    #~ if (error==0 and var != 0 and digits==None):
        #~ while(var < 0.1):
            #~ multiplied += 1
            #~ var *= 10
        #~ while(var > 10):
            #~ multiplied -= 1
            #~ var /= 10
    #~ if(debug): print("scale at error=0:", var, error)
    
    #~ # get the error to x.xxxx (10^0)
    #~ while(error < 1 and error != 0):
        #~ multiplied += 1
        #~ error *= 10
        #~ var *= 10
    #~ while(error > 10 and error != 0):
        #~ multiplied -= 1
        #~ error /= 10
        #~ var /= 10
    #~ if (debug): print("multiplied", multiplied)
    
    #~ if digits!=None:
        #~ while (digits > multiplied):
            #~ if debug: print("digits < multiplied -> multiplying some more")
            #~ var *= 10
            #~ error *= 10
            #~ multiplied += 1
        
    #~ # round the error to its first decimal place
    #~ error = round(error, 1)
    #~ if debug: print("initial_err_round:", error)
        
    #~ # for easy error analysis
    #~ error *= 10
    #~ var *= 10
    #~ multiplied += 1
        
    #~ # do the actual significance check...
    #~ var_ret, error_ret = round_to_significance_int_round(var, error, digits)
    #~ if debug: print("retvals of round:", var_ret, error_ret)
    
    #~ # better format the number and give out an exponent
    #~ exponent = (-1)*multiplied
    #~ if debug: print("exponent", exponent)
    #~ while (-3 <= exponent and exponent < 0):
        #~ error_ret /= 10
        #~ var_ret /= 10
        #~ exponent += 1
    #~ while (0 < exponent and exponent <= 3):
        #~ error_ret *= 10
        #~ var_ret *= 10
        #~ exponent -= 1

    #~ # if an exponent was given, scale back to it
    #~ if (use_exponent != None):
        #~ if (debug): print("use_exponent, exponent:", use_exponent, exponent)
        #~ while(exponent > use_exponent):
            #~ error_ret *= 10
            #~ var_ret *= 10
            #~ exponent -= 1
        #~ while(exponent < use_exponent):
            #~ error_ret /= 10
            #~ var_ret /= 10
            #~ exponent += 1
            
    #~ if debug: print("to_format:", var_ret, error_ret)
    #~ if debug: print("with (mult, expo):", multiplied, exponent)
    #~ if(digits==None):
        #~ if multiplied >= 0:
            #~ if exponent >= 0:
                #~ if debug: print("format_string:", "{0:=" + str(exponent) + ".f}")
                #~ var_ret = ("{0:."+str(exponent)+"f}").format(var_sgn*var_ret)
                #~ error_ret = ("{0:."+str(exponent)+"f}").format(error_ret)
            #~ else:
                #~ if debug: print("format_string:", "{0:.0f}")
                #~ var_ret = ("{0:.0f}").format(var_sgn*var_ret)
                #~ error_ret = ("{0:.0f}").format(error_ret)
        #~ else:
            #~ if exponent >= 0:
                #~ if debug: print("format_string:", "{0:.0f}")
                #~ var_ret = ("{0:.0f}").format(var_sgn*var_ret)
                #~ error_ret = ("{0:.0f}").format(error_ret)
            #~ else:
                #~ if debug: print("format_string:", "{0:.0f}")
                #~ var_ret = ("{0:.0f}").format(var_sgn*var_ret)
                #~ error_ret = ("{0:.0f}").format(error_ret)
    #~ else: # digits != None
        #~ exponent_rest = digits + exponent
        #~ if debug: print("to_format:", var_ret, error_ret)
        #~ if debug: print("with (mult, exponent_rest):", multiplied, exponent_rest)
        #~ if multiplied > 0:
            #~ if exponent_rest >= 0:
                #~ if debug: print("format_string:", "{0:=" + str(exponent_rest) + ".f}")
                #~ var_ret = ("{0:."+str(exponent_rest)+"f}").format(var_sgn*var_ret)
                #~ error_ret = ("{0:."+str(exponent_rest)+"f}").format(error_ret)
            #~ else:
                #~ while (exponent_rest<0):
                    #~ if debug: print("divde by 10 exponent_rest=:",exponent_rest)
                    #~ var_ret /= 10
                    #~ error_ret /= 10
                    #~ exponent_rest += 1
                    #~ exponent += 1
                #~ if debug: print("format_string:", "{0:.0f}")
                #~ var_ret = ("{0:.0f}").format(int(var_sgn*var_ret))
                #~ error_ret = ("{0:.0f}").format(int(error_ret))
        #~ else:
            #~ if exponent_rest >= 0:
                #~ if debug: print("format_string:", "{0:.0f}")
                #~ var_ret = ("{0:.0f}").format(var_sgn*var_ret)
                #~ error_ret = ("{0:.0f}").format(error_ret)
            #~ else:
                #~ if debug: print("format_string:", "{0:.0f}")
                #~ var_ret = ("{0:.0f}").format(var_sgn*var_ret)
                #~ error_ret = ("{0:.0f}").format(error_ret)
        
    #~ if error_was_none: error_ret = None
    #~ if (debug): print("result of rounding: ", (var_ret, error_ret))
    #~ return(var_ret, error_ret, exponent)
    
round_to_significance(15, 10)