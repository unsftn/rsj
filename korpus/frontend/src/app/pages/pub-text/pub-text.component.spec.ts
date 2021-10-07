import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PubTextComponent } from './pub-text.component';

describe('PubTextComponent', () => {
  let component: PubTextComponent;
  let fixture: ComponentFixture<PubTextComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PubTextComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PubTextComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
