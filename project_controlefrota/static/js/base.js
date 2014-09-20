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
