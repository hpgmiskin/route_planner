from shared import *
import reportContent

report = reportContent.ReportContent("report/test.tex")

report.titlePage()

report.section("Introduction")
report.introduction()
report.aimsObjectives()

report.section("Background Material")
report.problemOutline()
report.literatureReview()

report.section("Background Concepts")
report.latinHypercubeSampling()
report.exactTravellingSalesman()
report.dubinPathPlanning()

report.section("Method")
report.method()
report.energyModel()
report.exactTravellingPlane()
report.progressiveTravellingPlane()
report.planePathPlanning()

report.section("Results")
report.energyModelResults()
report.travellingPlaneResults()
report.pathPlanningResults()
report.modelResults()

report.section("Conclusions")
report.conclusions()

report.section("Report Methodology")
report.projectPlan()
report.documentWriting()
report.pythonCode()

report.bibliography()
report.addWordCount()

# report.compile(True)
