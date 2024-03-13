import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ButtonModule } from 'primeng/button';
import { ToolbarModule } from 'primeng/toolbar';
import { NgxParticlesModule } from '@tsparticles/angular';
import { ToolbarComponent } from './toolbar.component';

@NgModule({
  declarations: [ToolbarComponent],
  imports: [
    CommonModule,
    ButtonModule,
    ToolbarModule,
    NgxParticlesModule,
  ],
  exports: [ToolbarComponent]
})
export class MyToolbarModule { }
