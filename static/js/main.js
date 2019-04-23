M.AutoInit();

$('#add_ingredient').click(function() {
    var ing_id = $('#ingredients input:last').attr('id');
    var lastNameNum = parseInt(ing_id.substr(ing_id.length - 1));
    var nextNameNum = lastNameNum + 1;
    lastNameNum + 1;
    $('#ingredients').append('<tr><td><input name="ingredient_name' + nextNameNum + '" id="ingredient_name' + nextNameNum + '" type="text" class="validate"><label for="icon_prefix">Ingredient</label></td><td><input name="ingredient_amount' + nextNameNum + '" id="ingredient_amount' + nextNameNum + '" type="text" class="validate"><label for="ingredient_amount">Amount</label></td></tr>');
});

$('#add_step').click(function() {
    var step_id = $('#steps textarea:last').attr('id');
    var lastStepNum = parseInt(step_id.substr(step_id.length - 1));
    var nextStepNum = lastStepNum + 1;
    lastStepNum + 1;
    $('#steps').append('<tr><td><textarea name="step' + nextStepNum + '" id="step' + nextStepNum + '" type="text" class="materialize-textarea validate"></textarea><label for="step">STEP</label></td></tr>');
});
