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
        Schema::create('PROMOCIONES', function (Blueprint $table){
            $table->bigInteger('ID', true)->primary()->startingValue(10000);
            $table->string('Nombre', 20);
            $table->string('Tipo', 20);
            $table->decimal('Valor');
            $table->string('Estado', 1);
            $table->date('Fecha_ini');
            $table->date('Fecha_fin');
            $table->string('Descripcion', 100);
        });

        Schema::create('SUSCRIPCION', function (Blueprint $table){
            $table->bigInteger('ID', true)->primary()->startingValue(1);
            $table->string('Membresia', 20);
            $table->string('Plan', 10);
            $table->string('Descripcion', 40);
            $table->decimal('Precio');
        });

        Schema::create('PAGO', function (Blueprint $table){
            $table->bigInteger('ID', true)->primary()->startingValue(50000);
            $table->string('Metodo_de_pago',1);
            $table->date('Fecha');
            $table->decimal('Monto_total');

            $table->integer('ClienteID');
            $table->integer('AdministradorID');
            $table->bigInteger('SuscripcionID');
            $table->bigInteger('PromocionesID')->nullable();
            $table->string('Estado_pago',10);

            $table->foreign('PromocionesID')->references('ID')->on('PROMOCIONES')->onUpdate('cascade');
            $table->foreign('SuscripcionID')->references('ID')->on('SUSCRIPCION')->onUpdate('cascade');
            $table->foreign('ClienteID')->references('ID')->on('CLIENTE')->onUpdate('cascade');
            $table->foreign('AdministradorID')->references('ID')->on('ADMINISTRATIVO')->onUpdate('cascade');
        });

        Schema::create('COMPROBANTE', function (Blueprint $table){
            $table->bigInteger('ID', true)->primary()->startingValue(7000);
            $table->decimal('Monto');
            $table->date('Fecha_ini_mem');
            $table->date('Fecha_fin_mem');

            $table->bigInteger('PagoID');
            $table->integer('ClienteID');

            $table->foreign('PagoID')->references('ID')->on('PAGO')->onUpdate('cascade');
            $table->foreign('ClienteID')->references('ID')->on('CLIENTE')->onUpdate('cascade');
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
