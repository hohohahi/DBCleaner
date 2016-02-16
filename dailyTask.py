import parseDailyData
import getCurrentDepartmentPrice
import tool.sendEmail
officeTradeData = parseDailyData.getDailyTradeNumber()


dailyPrice = 'Current price:' + getCurrentDepartmentPrice.getDailyPrice()

output = officeTradeData + '-----' +  dailyPrice
tool.sendEmail.sendEmail(output, output)