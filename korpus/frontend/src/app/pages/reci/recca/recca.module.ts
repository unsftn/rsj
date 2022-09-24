import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { InputTextModule } from 'primeng/inputtext';
import { MyToolbarModule } from '../../toolbar/toolbar.module';
import { ReccaComponent } from './recca.component';

const routes: Routes = [{ path: '', component: ReccaComponent }]

@NgModule({
  declarations: [ReccaComponent],
  imports: [
    CommonModule,
    FormsModule,
    RouterModule.forRoot(routes),
    InputTextModule,
    MyToolbarModule,
  ],
  exports: [RouterModule],
  bootstrap: [ReccaComponent]
})
export class ReccaModule { }
