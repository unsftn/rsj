import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { InputTextModule } from 'primeng/inputtext';
import { MyToolbarModule } from '../../toolbar/toolbar.module';
import { UzvikComponent } from './uzvik.component';

const routes: Routes = [{ path: '', component: UzvikComponent }]

@NgModule({
  declarations: [UzvikComponent],
  imports: [
    CommonModule,
    FormsModule,
    RouterModule.forChild(routes),
    InputTextModule,
    MyToolbarModule,
  ],
  exports: [RouterModule],
  bootstrap: [UzvikComponent]
})
export class UzvikModule { }