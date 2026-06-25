<?php

namespace Database\Seeders;

use App\Models\User;
use App\UseCase\Administracion\AdminPerfil;
use App\UseCase\Usuarios\{AdminTipo, AdminUsuario};
// use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     */
    public function run(): void
    {
        // User::factory(10)->create();

        User::factory()->create([
            'name' => 'Test User',
            'email' => 'test@example.com',
        ]);

        $adminusuario = new AdminUsuario();
        $adminusuario->CrearUsuario(1234,'Messi','7123456', 'ejemplo@gmail.com',1,1,1,1,'2002-02-12','M');

        //obteniendo id del usuario creado
        $id = $adminusuario->GetIdByCI(1234);

        $admintipo = new AdminTipo();
        $admintipo->CrearAdmin($id,'na','na');
        $admintipo->CrearNutricionista($id,'na');
        $admintipo->CrearCliente($id,'premium','2002-02-02','2060-02-02');
        $admintipo->CrearInstructor($id,'na');

        $adminperfil = new AdminPerfil();
        $adminperfil->CrearPerfil('A','A','1234',$id,$id);
        $adminperfil->CrearPerfil('C','A','1234',$id,$id);
        $adminperfil->CrearPerfil('I','A','1234',$id,$id);
        $adminperfil->CrearPerfil('N','A','1234',$id,$id);
    }
}
