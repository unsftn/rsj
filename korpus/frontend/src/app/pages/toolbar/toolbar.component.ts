import { Component, Input, OnInit, Output, EventEmitter } from '@angular/core';
import { MenuItem, MessageService, PrimeNGConfig } from 'primeng/api';

@Component({
  selector: 'toolbar',
  templateUrl: './toolbar.component.html',
  styleUrls: ['./toolbar.component.scss']
})
export class ToolbarComponent implements OnInit {

  workflowItems: MenuItem[];
  @Input() title = '';
  @Output() saveClicked = new EventEmitter();

  constructor(
    private primengConfig: PrimeNGConfig,
    private messageService: MessageService,
  ) { }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
  }

  undoAvailable(): boolean {
    return true;
  }

  redoAvailable(): boolean {
    return true;
  }

  workflowDisabled(): boolean {
    return false;
  }

  undo(): void {
    this.notImplemented();
  }

  redo(): void {
    this.notImplemented();
  }

  preview(): void {
    this.notImplemented();
  }

  save(): void {
    this.saveClicked.emit();
  }

  delete(): void {
    this.notImplemented();
  }

  notImplemented(): void {
    this.messageService.add({
      severity: 'error',
      summary: 'Грешка',
      life: 5000,
      detail: `Још не ради`,
    });
  }
}
