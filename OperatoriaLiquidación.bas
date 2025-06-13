Public finalws As String
Public codJurisdiccion As String
Public coeficienteUnificadoDistribucion As Variant
Public baseImpo As String
Public outputPath As String
Public total As String
Public codAct As String
Public totalColumns As Integer
Public mainInitialRow As Integer
Public alicuota As String

Sub MostrarFormulario()
    UserForm1.Show
    LoopUntilNoResult
End Sub

Sub LoopUntilNoResult()
    Dim currentCell As Range
    Dim currentRow As Integer
    Dim currentColumn As Integer
    Dim currentSheet As String
    Dim wbOrigen As Workbook
    Dim wbOrigenDir As String
    
    Dim wsOrigen As Worksheet
    currentRow = 5
    
    Dim outputIncremental As Integer
    outputIncremental = 12
    
    Dim outputWs As Worksheet
    
    Dim ultimaColumna As Long, j As Long
    Dim codAdc As String
    
    Set currentCell = Range("A" & currentRow)
    
    ' Path del archivo core
    wbOrigenDir = ThisWorkbook.FullName
    Set wbOrigen = Workbooks.Open(wbOrigenDir)
    Set wsOrigen = wbOrigen.Sheets(finalws)
    ' Path del archivo Excel output
    'outputPath = "C:\Users\bmorales\OneDrive - rmrconsultores.com\Escritorio\AAAAAAAAAA.xlsx"
    Set wbOutput = Workbooks.Open(outputPath)
    
    ' Obtenemos todo de la row 3 a modo de ancla
    ultimaColumna = wsOrigen.Cells(3, wsOrigen.Columns.Count).End(xlToLeft).Column
    
    'Row inicial del primer codigo de Jurisdiccion
    mainInitialRow = 5
    'Column inicial del primer dato de Cod de Actividad
    currentColumn = 4
    
    ' While que trabaja la operatoria en torno a la column A
    Do While wsOrigen.Cells(mainInitialRow, 1).Value <> "" And LCase(wsOrigen.Cells(mainInitialRow, 1).Value) <> "TOTAL INGRESOS"
    
    ' Data que se rige por row
    codJurisdiccion = wsOrigen.Range("A" & currentRow).Value
    
    If Trim(codJurisdiccion) = "" Then
        Exit Do
    End If
    
    coeficienteUnificado = wsOrigen.Range("C" & currentRow).Value
    total = wsOrigen.Range("S" & currentRow).Value
    
    Worksheets("Template").Copy After:=Worksheets(Worksheets.Count)
    ActiveSheet.Name = codJurisdiccion
    currentSheet = ActiveSheet.Name
    
    ' Data que se rige por column
    ' Trabajamos lo obtenido en la row 3
    For j = 1 To ultimaColumna
        If InStr(1, wsOrigen.Cells(3, j).Value, "Serv", vbTextCompare) > 0 Then
            codAct = Trim(Split(wsOrigen.Cells(3, j).Value, "-")(0))
            
            
            ModifyData outputIncremental, currentSheet, codAct
            
            baseImpo = wsOrigen.Cells(currentRow, currentColumn).Value
            currentColumn = currentColumn + 1
            alicuota = wsOrigen.Cells(currentRow, currentColumn).Value * 100
                    
            AddColumnData outputIncremental, baseImpo, alicuota, currentSheet
            AddFinalData total, coeficienteUnificado, currentSheet
            
            
            outputIncremental = outputIncremental + 1
            currentColumn = currentColumn + 2
        End If
    Next j
    
    'Reset Values
    currentRow = currentRow + 1
    currentColumn = 4
    outputIncremental = 12
    
    'MsgBox "Finalizado Sheet para: " & codJurisdiccion
    
    Loop
    MsgBox "Operatoria Finalizada Exitosamente."
End Sub

Sub ModifyData(outputIncremental As Integer, currentWs As String, codAct As String)
'Se encarga de aplicar datos nulos en la tabla y el código de actividad

    Dim ws As Worksheet
    Set ws = Worksheets(currentWs)
    Dim wb As Workbook
    Set wb = ThisWorkbook
    
    ws.Range("B" & outputIncremental).Value = "0"
    ws.Range("C" & outputIncremental).Value = codAct
    ws.Range("D" & outputIncremental).Value = "0"
    ws.Range("F" & outputIncremental).Value = "0"
    
    ' Guardar cambios
    wb.Save
    ' wb.Close
    
End Sub

Sub AddFinalData(total As String, coeficienteUnificado As Variant, currentWs As String)
'Se encarga de aplicar los datos que no tienen repetición

    Dim ws As Worksheet
    Set ws = Worksheets(currentWs)
    Dim wb As Workbook
    Set wb = ThisWorkbook
    
    ws.Range("C3").Value = CDbl(coeficienteUnificado)
    ws.Range("C6").Value = CDbl(total)
    
    wb.Save

End Sub

Sub AddColumnData(outputIncremental As Integer, baseImpo As String, alicuota As String, currentWs As String)
'Se encarga de poner los datos con repetición

    Dim ws As Worksheet
    Set ws = Worksheets(currentWs)
    Dim wb As Workbook
    Set wb = ThisWorkbook
    
    ws.Range("E" & outputIncremental).Value = baseImpo
    ws.Range("G" & outputIncremental).Value = alicuota
    
    wb.Save

End Sub
