$uri = "https://contador-central.onrender.com/api/upload"

$leituras = @(

@{
    data = "2026-06-28T08:00:00"
    recepcao = 120000
    financeiro = 80000
},

@{
    data = "2026-06-30T08:00:00"
    recepcao = 122500
    financeiro = 82000
},

@{
    data = "2026-07-01T08:00:00"
    recepcao = 123800
    financeiro = 83500
},

@{
    data = "2026-07-02T08:00:00"
    recepcao = 124700
    financeiro = 84500
},

@{
    data = "2026-07-03T08:00:00"
    recepcao = 125420
    financeiro = 85214
}

)

foreach($l in $leituras){

    $body = @{

        unidade = "Gramado"

        impressoras = @(
            @{
                nome = "Recepção"
                modelo = "HP LaserJet M404"
                serial = "HP001"
                ip = "10.1.1.15"
                contador = $l.recepcao
                data = $l.data
            },
            @{
                nome = "Financeiro"
                modelo = "Brother L6900"
                serial = "BR001"
                ip = "10.1.1.16"
                contador = $l.financeiro
                data = $l.data
            }
        )

    } | ConvertTo-Json -Depth 5

    Write-Host ""
    Write-Host "Enviando leitura de $($l.data)..."

    $resp = Invoke-RestMethod `
        -Uri $uri `
        -Method POST `
        -ContentType "application/json; charset=utf-8" `
        -Body $body

    Write-Host "Resposta:" $resp.status
}