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
        Schema::create('USUARIO', function (Blueprint $table) {
            $table->integer('ID', true)->primary()->startingValue(20000);
            $table->integer('CI');
            $table->string('Nombre', 40);
            $table->string('Telefono', 8)->nullable();
            $table->string('Correo', 40);
            $table->boolean('RolC');
            $table->boolean('RolI');
            $table->boolean('RolN');
            $table->boolean('RolA');
            $table->date('Fecha_Nacimiento');
            $table->string('Sexo', 1);
        });

        Schema::create('ADMINISTRATIVO', function (Blueprint $table) {
            $table->integer('ID')->primary();
            $table->string('Cargo', 20);
            $table->string('Turno', 6);
            $table->foreign('ID')->references('ID')->on('USUARIO')->onUpdate('cascade');
            // foreign key (id) references usuario(ID);
        });

        Schema::create('CLIENTE', function (Blueprint $table) {
            $table->integer('ID')->primary();
            $table->string('Suscripcion', 10)->nullable();
            $table->date('Fecha_ini_mem')->nullable();
            $table->date('Fecha_fin_mem')->nullable();
            //$table->date('Fecha_de_nacimiento');
            $table->foreign('ID')->references('ID')->on('USUARIO')->onUpdate('cascade');
        });

        Schema::create('INSTRUCTOR', function (Blueprint $table) {
            $table->integer('ID')->primary();
            $table->string('Especialidad', 25);
            $table->foreign('ID')->references('ID')->on('USUARIO')->onUpdate('cascade');
        });

        Schema::create('NUTRICIONISTA', function (Blueprint $table) {
            $table->integer('ID')->primary();
            $table->string('Horario_atencion', 50);
            $table->foreign('ID')->references('ID')->on('USUARIO')->onUpdate('cascade');
        });

        Schema::create('PERFIL', function (Blueprint $table) {
            $table->integer('ID', true)->primary()->startingValue(10001); //autoincrement
            $table->string('Estado', 1);
            $table->string('Tipo', 1);
            $table->string('Contrasena', 15);
            $table->integer('UsuarioID');
            $table->integer('AdminID');

            $table->foreign('UsuarioID')->references('ID')->on('USUARIO')->onUpdate('cascade');
            $table->foreign('AdminID')->references('ID')->on('ADMINISTRATIVO')->onUpdate('cascade');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        //

        Schema::dropIfExists('DETALLE_RUTINA');
        Schema::dropIfExists('SEGUIMIENTO');
        Schema::dropIfExists('ANTECEDENTES');
        Schema::dropIfExists('RESERVA');
        Schema::dropIfExists('HORARIO');
        Schema::dropIfExists('DISCIPLINA');
        Schema::dropIfExists('SALA');
        Schema::dropIfExists('EJERCICIOS');
        Schema::dropIfExists('RUTINA');

        Schema::dropIfExists('COMPROBANTE');
        Schema::dropIfExists('PAGO');
        Schema::dropIfExists('SUSCRIPCION');
        Schema::dropIfExists('PROMOCIONES');

        Schema::dropIfExists('PERFIL');
        Schema::dropIfExists('CLIENTE');
        Schema::dropIfExists('INSTRUCTOR');
        Schema::dropIfExists('NUTRICIONISTA');
        Schema::dropIfExists('ADMINISTRATIVO');
        Schema::dropIfExists('USUARIO');
    }
};
