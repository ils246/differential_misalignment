*/ DATA IMPORT
import delimited "C:\Users\Roberto Vestrelli\Desktop\GITHUB\STATA\regression_1_data.csv", clear 
gen country_dom = country
encode country, gen(country_)
encode model, gen(model_)

* MODEL DUMMIES
gen RSF = 0
gen MISTRAL = 0
gen DEEPSEEK = 0
gen GEMINI = 0
gen QWEN = 0
gen FALCON = 0
gen GPT = 0
replace RSF = 1 if model == "RSF"
replace MISTRAL = 1 if model == "MISTRAL"
replace DEEPSEEK = 1 if model == "DEEPSEEK"
replace GEMINI = 1 if model == "GEMINI"
replace QWEN = 1 if model == "QWEN"
replace FALCON = 1 if model == "FALCON"
replace GPT = 1 if model == "GPT"

* COUNTRY DUMMIES
gen dummy_uae = 0
gen dummy_china = 0
gen dummy_us = 0
gen dummy_france = 0
replace dummy_uae = 1 if country == "United Arab Emirates"
replace dummy_china = 1 if country == "China"
replace dummy_us = 1 if country == "United States"
replace dummy_france = 1 if country == "France"


* REGRESSIONS
* full sample
areg scores b0.(model_)##(dummy_china dummy_us dummy_uae dummy_france) scores_rsf if type == "original", absorb(country_) vce(cluster country_)
eststo model1 

esttab model1 using regression_1_results.csv, replace nobaselevels se label ///
    star(* 0.1 ** 0.05 *** 0.01) ///
    keep(1.model_ 2.model_ 3.model_ 4.model_ 5.model_ 6.model_ *#* scores_rsf) ///
    noomitted stats(r2 N, labels("R-squared" "Observations")) ///
    mlabels("Full Sample" "Variations (Sub Sample)")
	
* VARIATIONS
egen keep_countries = max(type == "variation1"), by(country)

areg scores b0.(model_)##(dummy_china dummy_us dummy_uae dummy_france) scores_rsf if type == "original" & keep_countries == 1, absorb(country_) vce(cluster country_)
eststo model1 
areg scores b0.(model_)##(dummy_china dummy_us dummy_uae dummy_france) scores_rsf if type == "variation1" & keep_countries == 1, absorb(country_) vce(cluster country_)
eststo model2 
areg scores b0.(model_)##(dummy_china dummy_us dummy_uae dummy_france) scores_rsf if type == "variation2" & keep_countries == 1, absorb(country_) vce(cluster country_)
eststo model3
esttab model1 model2 model3 using regression_2_results.csv, replace nobaselevels se label ///
    star(* 0.1 ** 0.05 *** 0.01) ///
    keep(1.model_ 2.model_ 3.model_ 4.model_ 5.model_ 6.model_ *#* scores_rsf) ///
    noomitted stats(r2 N, labels("R-squared" "Observations")) ///
    mlabels("Original" "Randomization 1" "Randomization 2")
