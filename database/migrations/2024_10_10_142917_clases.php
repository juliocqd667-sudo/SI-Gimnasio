<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        //
        Schema::create('ANTECEDENTES', function (Blueprint $table){
            $table->bigInteger('ID', true)->primary();
            $table->date('Fecha');
            $table->text('Diagnostico');
            $table->text('Recomendaciones');
            $table->text('Objetivo');
            $table->decimal('Peso');
            $table->decimal('Altura');
            $table->decimal('IMC');
            $table->decimal('GC');
            $table->decimal('MM');
            $table->date('Fecha_Prox_Consulta');

            $table->integer('ClienteID');
            $table->integer('NutricionistaID');
            
            $table->foreign('ClienteID')->references('ID')->on('CLIENTE')->onUpdate('cascade');
            $table->foreign('NutricionistaID')->references('ID')->on('NUTRICIONISTA')->onUpdate('cascade');
        });

        Schema::create('RUTINA', function (Blueprint $table){
            $table->bigInteger('ID', true)->primary()->startingValue(100);
            $table->string('Nombre', 20);
            $table->string('Descripcion', 255);
        });

        Schema::create('EJERCICIOS', function (Blueprint $table){
            $table->bigInteger('ID', true)->primary()->startingValue(500);
            $table->string('Nombre', 30);
            $table->string('Descripcion', 255);
            
        });

        Schema::create('DETALLE_RUTINA', function (Blueprint $table){
            $table->bigInteger('ID', true)->primary()->startingValue(6000);
            $table->string('Dia',9);
            $table->string('Repeticiones',2);
            $table->string('Serie',2);
            $table->string('Peso',5);
            
            $table->bigInteger('RutinaID');
            $table->bigInteger('EjerciciosID');
            
            $table->foreign('RutinaID')->references('ID')->on('RUTINA')->onUpdate('cascade');
            $table->foreign('EjerciciosID')->references('ID')->on('EJERCICIOS')->onUpdate('cascade');
        });

        Schema::create('SALA', function (Blueprint $table){
            $table->bigInteger('ID', true)->primary()->startingValue(1);
            $table->string('Descripcion',100);
            $table->integer('Capacidad');
        });

        Schema::create('DISCIPLINA', function (Blueprint $table){
            $table->bigInteger('ID', true)->startingValue(2001)->primary();
            $table->string('Nombre',20);
            $table->integer('Grupo');
            $table->integer('Cupo');
            $table->text('Hora_Inicial');
            $table->text('Hora_Final');
            $table->bigInteger('SalaID');
            $table->foreign('SalaID')->references('ID')->on('SALA')->onUpdate('cascade');
        });

        Schema::create('HORARIO', function (Blueprint $table){
            $table->bigInteger('ID', true)->primary()->startingValue(15000);
            $table->string('Dia', 9);
            $table->time('Hora_Inicial');
            $table->time('Hora_Final');
            
            $table->bigInteger('DisciplinaID');

            $table->foreign('DisciplinaID')->references('ID')->on('DISCIPLINA')->onUpdate('cascade');
        });

        Schema::create('RESERVA', function (Blueprint $table){
            $table->bigInteger('ID', true)->primary()->startingValue(800);
            $table->date('Fecha');
            $table->string('Estado', 1);

            $table->integer('ClienteID');
            $table->bigInteger('DisciplinaID');
            $table->bigInteger('ComprobanteID');

            $table->foreign('ClienteID')->references('ID')->on('CLIENTE')->onUpdate('cascade');
            $table->foreign('DisciplinaID')->references('ID')->on('DISCIPLINA')->onUpdate('cascade');
            $table->foreign('ComprobanteID')->references('ID')->on('COMPROBANTE')->onUpdate('cascade');
        });

        Schema::create('SEGUIMIENTO', function(Blueprint $table){
            $table->bigInteger('ID', true)->primary()->startingValue(1500);
            $table->date('Fecha');
            $table->text('Observaciones');
            $table->text('Objetivo');
            $table->date('Fecha_Prox_Consulta');

            $table->integer('ClienteID');
            $table->integer('InstructorID');
            $table->bigInteger('RutinaID');

            $table->foreign('ClienteID')->references('ID')->on('CLIENTE')->onUpdate('cascade');
            $table->foreign('InstructorID')->references('ID')->on('INSTRUCTOR')->onUpdate('cascade');
            $table->foreign('RutinaID')->references('ID')->on('RUTINA')->onUpdate('cascade');
        });

    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        //
    }
};
