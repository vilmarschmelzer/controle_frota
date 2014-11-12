$(document).ready(function(){
	path = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');

    $('#estado_origem').change(function(){

        $.ajax({

        url: path+"/estado/cidades/", // url
        type: 'POST',
        dataType: 'json',
        data: {estado: $(this).val()},
        beforeSend: function() {
            $("#cidade_origem").html("<option value=''>Carregando...</option>");
        },
        success: function(data, textStatus, xhr) {

            var html = null;
            var cidade = data;

            html += '<option selected="selected" value="">Selecione uma Cidade</option>'
            $(cidade).each(function(key,val){
                html += '<option value="'+val.pk+'">'+val['fields']['nome']+'</option>';
            });
            $('#cidade_origem').html( html );

        },
        error: function(xhr, textStatus, errorThrown) {
            $('#cidade_origem').html( '<option value="">Nenhuma cidade cadastrada para este estado</option>' );
            }
        });
    });

    $('#estado_destino').change(function(){

        $.ajax({

        url: path+"/estado/cidades/", // url
        type: 'POST',
        dataType: 'json',
        data: {estado: $(this).val()},
        beforeSend: function() {
            $("#cidade_destino").html("<option value=''>Carregando...</option>");
        },
        success: function(data, textStatus, xhr) {

            var html = null;
            var cidade = data;

            console.log(data);

            html += '<option selected="selected" value="">Selecione uma Cidade</option>'
            $(cidade).each(function(key,val){
                html += '<option value="'+val.pk+'">'+val['fields']['nome']+'</option>';
            });
            $('#cidade_destino').html( html );

        },
        error: function(xhr, textStatus, errorThrown) {
            $('#cidade_destino').html( '<option value="">Nenhuma cidade cadastrada para este estado</option>' );
            }
        });
    });
});

function buscar_veiculos(){

    path = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');

    var data = {};

    data["dt_devolucao_day"] = $("select[name=dt_devolucao_day]").val();

    data['dt_devolucao_month'] = $("select[name=dt_devolucao_month]").val();
    data['dt_devolucao_year'] = $("select[name=dt_devolucao_year]").val();
    data['hora_devolucao'] = $("input[name=hora_devolucao]").val();

    data['dt_saida_day'] = $("select[name=dt_saida_day]").val();
    data['dt_saida_month'] = $("select[name=dt_saida_month]").val();
    data['dt_saida_year'] = $("select[name=dt_saida_year]").val();
    data['hora_saida'] = $("input[name=hora_saida]").val();

    $.ajax({

        url: path+"/emprestimo/veiculos/", // url
        type: 'POST',
        dataType: 'json',
        data: data,
        beforeSend: function() {

        },
        success: function(data, textStatus, xhr) {

            if(data.success == undefined){
                var html = '';

                html += '<select name="veiculo" class="form-control"><option selected="selected" value="">Selecione um veículo</option>';

                $(data).each(function(key,val){
                    html += '<option value="'+val.pk+'">'+val['fields']['nome']+'</option>';
                });
                html += '</select>';
                $("#veiculos").html(html);
                $("#alerta").html('');
            }
            else{
                $("#alerta").html(data.msg);
            }
        },
        error: function(xhr, textStatus, errorThrown) {
            $('#veiculos').html('Erro ao buscar veículos');
        }
    });
}

    $('#usuario').blur(function() {

	    var url=path+'/cliente/validausuario/';

	    if(document.getElementById("id") != null){
			console.log($('#id').val());
			url+=$('#id').val()+'/';
		}

	    $.ajax({
	    	url: url,
	        type: 'POST',
	        dataType: 'json',
	        data: $('#usuario'),
	        success: function (response, textStatus, xhr) {
	        	$('#field_usuario').html(response.html);
	        },
	        error : function(jqXHR, textStatus, errorThrown){
	            alert('error: ' + textStatus + errorThrown);
	        }
	    });
	});

    $('#pesquisa_valor').blur(function() {

        action = $('#formProcurar').attr('action');
        href_servidor= '/imprimir-relatorio-servidores/';
        href_veiculo= '/imprimir-relatorio-veiculos/';

        href = '';

        if(action == '/relatorio-servidores/'){
            $('#print_relatorio_servidores').attr('href', href_servidor+'?valor='+$('#pesquisa_valor').val());
        }
        else{
            $('#print_relatorio_servidores').attr('href', href_veiculo+'?valor='+$('#pesquisa_valor').val());
        }

    });