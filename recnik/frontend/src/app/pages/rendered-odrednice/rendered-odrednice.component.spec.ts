import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RenderedOdredniceComponent } from './rendered-odrednice.component';

describe('RenderedOdredniceComponent', () => {
  let component: RenderedOdredniceComponent;
  let fixture: ComponentFixture<RenderedOdredniceComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RenderedOdredniceComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RenderedOdredniceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
