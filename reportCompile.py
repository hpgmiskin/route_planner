from shared import *
import reportContent

report = reportContent.ReportContent("report/ref1.tex")

# report.titlePage()

# report.section("Introduction")
# report.introduction()
# report.aimsObjectives()

# report.section("Background Material")
# report.problemOutline()
# report.literatureReview()

# report.section("Background Concepts")
# report.latinHypercubeSampling()
# report.exactTravellingSalesman()
# report.dubinPathPlanning()

# report.section("Method")
# report.method()
# report.energyModel()
# report.exactTravellingPlane()
# report.progressiveTravellingPlane()
# report.planePathPlanning()

# report.section("Results")
# report.energyModelResults()
# report.travellingPlaneResults()
# report.pathPlanningResults()
# report.modelResults()

# report.section("Conclusions")
# report.conclusions()

# report.section("Report Methodology")
# report.projectPlan()
# report.documentWriting()
# report.pythonCode()

# report.paragraph(r"\citen{M.Price2006} \citen{Asselin1997} \citen{Raymer2006} \citen{Dubins1957} \citen{Boissonnat1993} \citen{Chitsaz2007} \citen{Bigg1976} \citen{Held1984} \citen{DeBerg2010} \citen{McGee2005} \citen{LeNy2008} \citen{Chakrabarty2009}")
report.paragraph(r"\citen{Al-Sabban} \citen{Techy2009} \citen{Savla2005}")
# report.paragraph(r"\citen{Asselin1997} \citen{Bigg1976} \citen{Dubins1957} \citen{Forrester2008}")
report.bibliography()
# report.addWordCount(9924)

report.compile(True)