Attribute VB_Name = "Module1"
Option Explicit

Sub single_year_stock_loop()

Rem - Define variables

Dim ws As Worksheet
Dim output_range, yearly_change, inc_ticker, inc_value, dec_ticker, dec_value, great_vol_tikcer, greate_vol_value, time_elapse As Range
Dim start_time, end_time, numYear, numRow, i, numTicker, begin_price, ending_price As Double
Dim yearlist(2) As String

start_time = Now()

'Set up year list array
yearlist(0) = "2014"
yearlist(1) = "2015"
yearlist(2) = "2016"

Rem - Loop through every year

For numYear = 0 To 2

    Set ws = Worksheets(yearlist(numYear))
    Set output_range = ws.Range("I:Q")
    Set inc_ticker = ws.Range("P2")
    Set inc_value = ws.Range("Q2")
    Set dec_ticker = ws.Range("P3")
    Set dec_value = ws.Range("Q3")
    Set great_vol_tikcer = ws.Range("P4")
    Set greate_vol_value = ws.Range("Q4")
    Set time_elapse = ws.Range("O9")
    
    Rem - Clear Old Contents
    
    output_range.ClearContents
    
    Rem - Set up column/row names
    
    ws.Range("I1").Resize(, 4) = Array("Ticker", "Yearly Change", "Percent Change", "Total Stock Volume")
    
    ws.Range("P1").Resize(, 2) = Array("Ticker", "Value")
    
    ws.Range("O2").Value = "Greatest % Increase"
    ws.Range("O3").Value = "Greatest % Decrease"
    ws.Range("O4").Value = "Greatest Total Volume"
    
    ws.Range("O8").Value = "Time Elapsed"
    
    Rem - For loop begin
    
    'Count number of rows
    '1st methond to find the number of rows (The dataframe has to be continuous.)
    numRow = Cells(Rows.Count, 1).End(xlUp).Row
                        
                       
    '2nd method to find the number of rows (blank is okay)
    'It's looking for a 'wildcard' (any text), from the very bottom of the excel Cell XFD1048576.
    'and work its way up. Essentially it's from Control+F.=VLO
    'Source https://www.excelcampus.com/vba/find-last-row-column-cell/
    
    numRow = Cells.Find(What:="*", _
                    After:=Range("A1"), _
                    LookAt:=xlPart, _
                    LookIn:=xlFormulas, _
                    SearchOrder:=xlByRows, _
                    SearchDirection:=xlPrevious, _
                    MatchCase:=False).Row
    
    ''Sort Data first by ticker and then by date
    ''This step is needed because how I calculate yearly change and percentage change
    ''It takes forever. Muted this section for now
    'ws.Sort.SortFields.Add2 Key:=Range( _
    '    "A2:" & numRow), SortOn:=xlSortOnValues, Order:=xlAscending, DataOption:= _
    '    xlSortNormal
    'ActiveWorkbook.Worksheets("2014").Sort.SortFields.Add2 Key:=Range( _
    '    "B2:" & numRow), SortOn:=xlSortOnValues, Order:=xlAscending, DataOption:= _
    '    xlSortNormal
    'With ws.Sort
    '    .SetRange Range("A1:" & numRow)
    '    .Header = xlYes
    '    .MatchCase = False
    '    .Orientation = xlTopToBottom
    '    .SortMethod = xlPinYin
    '    .Apply
    'End With
    
    
    'For loop
    
    numTicker = 2                       'initialize numTicker
    begin_price = ws.Cells(2, 3).Value  'initialize first ticker's begin price
    
    For i = 2 To numRow
    
        'Get tickers, yearly change and pct change
        If ws.Cells(i, 1).Value <> ws.Cells(i + 1, 1).Value Then
                
            'print ticker
            ws.Range("I" & numTicker).Value = ws.Cells(i, 1).Value
    
            'print Yearly Change
            ending_price = ws.Cells(i, 6).Value
            ws.Range("J" & numTicker).Value = ending_price - begin_price
            
            'print pct change
            If begin_price <> 0 Then
                ws.Range("K" & numTicker).Value = ending_price / begin_price - 1
            Else
                ws.Range("K" & numTicker).Value = "" 'Temp fix for Ticker PLNT
            End If
            
            'print total stock volume
            ws.Range("L" & numTicker).FormulaR1C1 = "=SUMIFS(C7, C1, RC9)"
            
            'Gratest % increase
            If ws.Range("K" & numTicker).Value > 0 And ws.Range("K" & numTicker).Value > inc_value Then
                inc_ticker.Value = ws.Range("I" & numTicker)
                inc_value.Value = ws.Range("K" & numTicker)
            End If
            
            'Gratest % decrease
            If ws.Range("K" & numTicker).Value < 0 And ws.Range("K" & numTicker).Value < dec_value Then
                dec_ticker.Value = ws.Range("I" & numTicker)
                dec_value.Value = ws.Range("K" & numTicker)
            End If
            
            'Greatest % Total Volume
            If ws.Range("L" & numTicker).Value > greate_vol_value Then
                great_vol_tikcer.Value = ws.Range("I" & numTicker)
                greate_vol_value.Value = ws.Range("L" & numTicker)
            End If
            
            'Next ticker row
            numTicker = numTicker + 1
            
            'reset begin price
            begin_price = ws.Cells(i + 1, 3).Value
            
        
        End If
        
    Next i
    
    Rem - Conditional formatting
    
    Set yearly_change = ws.Range("J2:J" & numTicker)
    
    'Change > 0 fill to Green
    yearly_change.FormatConditions.Add Type:=xlCellValue, Operator:=xlGreater, Formula1:="=0"
    yearly_change.FormatConditions(yearly_change.FormatConditions.Count).SetFirstPriority
    With yearly_change.FormatConditions(1).Interior
        .PatternColorIndex = xlAutomatic
        .ThemeColor = xlThemeColorAccent6
        .TintAndShade = 0
    End With
    
    'Change <0 fill to Red
    yearly_change.FormatConditions(1).StopIfTrue = False
    yearly_change.FormatConditions.Add Type:=xlCellValue, Operator:=xlLess, Formula1:="=0"
    yearly_change.FormatConditions(yearly_change.FormatConditions.Count).SetFirstPriority
    With yearly_change.FormatConditions(1).Interior
        .PatternColorIndex = xlAutomatic
        .Color = 255
        .TintAndShade = 0
    End With
    
    Rem - Time to complete (in seconds)
    
    end_time = Round((Now() - start_time) * 24 * 60 * 60, 0)
    time_elapse.Value = end_time
    
Next numYear
End Sub
